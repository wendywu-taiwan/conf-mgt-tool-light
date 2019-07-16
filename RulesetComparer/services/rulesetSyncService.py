from django.template.loader import render_to_string

from RulesetComparer.b2bRequestTask.downloadRulesetTask import DownloadRulesetTask
from RulesetComparer.dataModel.dataObject.rulesetLogGroupObj import RulesetLogGroupObj
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.utils.timeUtil import *
from RulesetComparer.utils.fileManager import *
from RulesetComparer.properties.dataKey import *
from RulesetComparer.b2bRequestTask.compareRuleListTask import CompareRuleListTask
from RulesetComparer.b2bRequestTask.createRulesetTask import CreateRulesetTask
from RulesetComparer.b2bRequestTask.updateRulesetTask import UpdateRulesetTask
from RulesetComparer.b2bRequestTask.clearRulesetTask import ClearRulesetTask
from RulesetComparer.dataModel.dataParser.createRulesetSyncSchedulerParser import CreateRulesetSyncSchedulerParser
from RulesetComparer.dataModel.dataParser.applyRulesetToServerParser import ApplyRulesetToServerParser
from RulesetComparer.dataModel.dataBuilder.rulesetSyncPreDataBuilder import RulesetSyncPreDataBuilder
from RulesetComparer.dataModel.dataBuilder.rulesetSyncResultDataBuilder import RulesetSyncResultDataBuilder
from RulesetComparer.dataModel.dataParser.recoverRulesetsParser import RecoverRulesetsParser
from RulesetComparer.dataModel.dataBuilder.recoverRulesetsResultBuilder import RecoverRulesetsResultBuilder
from RulesetComparer.properties.dataKey import STATUS_SUCCESS, STATUS_FAILED
from RulesetComparer.dataModel.dataBuilder.diffUpdateRulesetBuilder import DiffUpdateRulesetBuilder
from RulesetComparer.dataModel.dataBuilder.diffCreateRulesetBuilder import DiffCreateRulesetBuilder


def create_ruleset_test():
    try:
        ruleset_xml = load_server_ruleset_with_name("INT1", "TW", 279984339, "TEST_WENDY")
        environment = Environment.objects.get(name="INT1")
        country = Country.objects.get(name="TW")
        result_obj = CreateRulesetTask(environment, country, "TEST_WENDY", ruleset_xml).get_result_data()
        print("create ruleset result:" + str(result_obj))
    except Exception as e:
        raise e


def update_ruleset_test():
    try:
        ruleset_name = "RS_TW_COPY_INTO_EXISTING_CASE_TOOLBAR"
        # source_xml = load_git_ruleset_with_name("TW", ruleset_name)
        source_xml = load_server_ruleset_with_name("INT1", "TW", 277570182, ruleset_name)
        target_xml = load_server_ruleset_with_name("TEST", "TW", 277570182, ruleset_name)
        environment = Environment.objects.get(name="TEST")
        country = Country.objects.get(name="TW")

        diff_json = RulesetComparer(ruleset_name, source_xml, target_xml, is_module=False).get_data_by_builder()
        target_only_rules_count = diff_json["target_env_only_rules"]["count"]

        if target_only_rules_count > 0:
            # clear ruleset first to remove deleted ruleset at target env
            result_obj = ClearRulesetTask(environment, country, ruleset_name).get_result_data()
            if result_obj.get("exception") is not None:
                return

        result_obj = UpdateRulesetTask(environment, country, ruleset_name, source_xml, target_xml,
                                       diff_json).get_result_data()
        print("create ruleset result:" + str(result_obj))
    except Exception as e:
        raise e


def sync_up_rulesets_without_scheduler(json_data, user):
    parser = CreateRulesetSyncSchedulerParser(json_data, user)
    for country in parser.country_list:
        try:
            rs_log_groups = RulesetLogGroupObj(parser, user, country)
            rs_log_groups.log_group()

            result_data = sync_up_rulesets(rs_log_groups, parser, country)
            send_mail(result_data, parser.receiver_list)
        except Exception as e:
            error_log(e)
            error_log(traceback.format_exc())


def sync_up_rulesets(rs_log_group, parser, country):
    compare_report_json = CompareRuleListTask(parser.source_environment_id,
                                              parser.target_environment_id,
                                              country.id).get_report()

    sync_up_report_json = RulesetSyncPreDataBuilder(compare_report_json).get_data()

    if sync_up_report_json is None:
        raise Exception("can not generate ruleset sync pre data")

    backup_rulesets(rs_log_group.backup_key, sync_up_report_json)
    sync_result_obj = RulesetsSyncResultListObj()
    # create rulesets
    if parser.action.create_ruleset:
        rulesets = sync_up_report_json[KEY_SOURCE_ENV_ONLY_RULESETS][KEY_RULESETS_ARRAY]
        sync_result_obj = create_rulesets(sync_result_obj, rs_log_group, country, parser.target_environment, rulesets)
    # update rulesets
    if parser.action.update_ruleset:
        rulesets = sync_up_report_json[KEY_DIFFERENT_RULESETS][KEY_RULESETS_ARRAY]
        sync_result_obj = update_rulesets(sync_result_obj, rs_log_group, country, parser.target_environment, rulesets)
    # delete rulesets
    if parser.action.delete_ruleset:
        pass
    rs_log_group.update_log_group_log_count()
    builder = RulesetSyncResultDataBuilder(sync_up_report_json, sync_result_obj)
    return builder.get_data()


def sync_up_rulesets_from_backup(json_data, user):
    parser = RecoverRulesetsParser(json_data)
    return sync_backup_rulesets(parser, user)


def sync_up_ruleset_from_backup(json_data, user):
    parser = ApplyRulesetToServerParser(json_data)
    return sync_backup_rulesets(parser, user)


def sync_backup_rulesets(parser, user):
    sync_result_obj = RulesetsSyncResultListObj()

    country = parser.country
    target_environment = parser.target_environment
    compare_key = hash(get_current_timestamp())

    rs_log_group = RulesetLogGroupObj(parser, user, parser.country)
    rs_log_group.log_group()

    new_backup_key = rs_log_group.backup_key

    server_rs_path = get_rule_set_path(target_environment.name, country.name, compare_key)
    server_rs_backup_path = get_backup_path_server_version(new_backup_key)
    applied_rs_path = parser.ruleset_path
    applied_rs_backup_path = get_backup_path_applied_version(new_backup_key)

    create_ruleset_list = []
    update_ruleset_list = []

    # backup deleted last time but created now ruleset
    for ruleset_name in parser.rulesets:
        # download ruleset server version
        ruleset_exist = DownloadRulesetTask(target_environment.id, country.id, ruleset_name, compare_key).ruleset_exist

        # if server not having ruleset, add to create ruleset list
        if ruleset_exist is False:
            create_ruleset_data = DiffCreateRulesetBuilder(ruleset_name).get_data()
            create_ruleset_list.append(create_ruleset_data)
            continue

        # backup applied backup ruleset from backup folder to new backup folder
        copy_ruleset(get_file_name("_xml", ruleset_name), applied_rs_path, applied_rs_backup_path)

        # backup server version ruleset from ruleset folder to backup folder
        copy_ruleset(get_file_name("_xml", ruleset_name), server_rs_path, server_rs_backup_path)

        source_xml = load_backup_applied_version_rs(new_backup_key, ruleset_name)
        target_xml = load_backup_server_version_rs(new_backup_key, ruleset_name)

        ruleset_comparer = RulesetComparer(ruleset_name, source_xml, target_xml, False)
        update_ruleset_data = DiffUpdateRulesetBuilder(ruleset_comparer).get_data()
        update_ruleset_list.append(update_ruleset_data)

    # create not exist rulesets
    sync_result_obj = create_rulesets(sync_result_obj, rs_log_group, country, target_environment, create_ruleset_list)
    # update rulesets
    sync_result_obj = update_rulesets(sync_result_obj, rs_log_group, country, target_environment, update_ruleset_list)

    # update rulesets count
    rs_log_group.update_log_group_log_count()
    builder = RecoverRulesetsResultBuilder(target_environment, country, sync_result_obj)
    return builder.get_data()


def backup_rulesets(backup_key, sync_up_pre_json):
    try:
        target_env_name = sync_up_pre_json[KEY_TARGET_ENV][KEY_NAME]
        source_env_name = sync_up_pre_json[KEY_SOURCE_ENV][KEY_NAME]
        country_name = sync_up_pre_json[KEY_COUNTRY][KEY_NAME]
        compare_key = sync_up_pre_json[KEY_COMPARE_HASH_KEY]
        source_env_only_rulesets = sync_up_pre_json[KEY_SOURCE_ENV_ONLY_RULESETS][KEY_RULESETS_ARRAY]
        target_env_only_rulesets = sync_up_pre_json[KEY_TARGET_ENV_ONLY_RULESETS][KEY_RULESETS_ARRAY]
        different_rulesets = sync_up_pre_json[KEY_DIFFERENT_RULESETS][KEY_RULESETS_ARRAY]

        server_rs_path = get_rule_set_path(target_env_name, country_name, compare_key)
        server_rs_backup_path = get_backup_path_server_version(backup_key)

        if source_env_name == GIT_NAME:
            source_rs_path = get_rule_set_git_path(country_name)
        else:
            source_rs_path = get_rule_set_path(source_env_name, country_name, compare_key)
        source_rs_backup_path = get_backup_path_applied_version(backup_key)

        # backup source environment only rs (it will create new ruleset to target env)
        for ruleset_obj in source_env_only_rulesets:
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), source_rs_path, source_rs_backup_path)

        # backup target environment only rs (it will be delete)
        # for ruleset_obj in target_env_only_rulesets:
        #     copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), server_rs_path, server_rs_backup_path)

        # backup different ruleset in both env
        for ruleset_obj in different_rulesets:
            # backup rs on server version
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), server_rs_path, server_rs_backup_path)
            # backup rs will be applied to server version
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), source_rs_path, source_rs_backup_path)

        # save pre sync json to backup folder
        save_auto_sync_pre_json_file(get_sync_pre_data_path(backup_key), sync_up_pre_json)
    except Exception as e:
        raise e


def create_rulesets(sync_result_obj, rs_log_group, country, target_environment, rulesets):
    if len(rulesets) == 0:
        return sync_result_obj

    for ruleset_obj in rulesets:
        ruleset_name = ruleset_obj["name"]
        ruleset_xml = load_backup_applied_version_rs(rs_log_group.backup_key, ruleset_name)

        result_obj = CreateRulesetTask(target_environment, country, ruleset_name, ruleset_xml).get_result_data()

        # add ruleset log
        rs_log_group.log(ruleset_name, RULESET_CREATE, result_obj.get(KEY_STATUS), result_obj.get(KEY_EXCEPTION))

        if result_obj.get(KEY_STATUS) == STATUS_SUCCESS:
            sync_result_obj.created_list.append(result_obj)
        else:
            sync_result_obj.failed_list.append(result_obj)

    return sync_result_obj


def update_rulesets(sync_result_obj, rs_log_group, country, target_environment, rulesets):
    for ruleset_obj in rulesets:
        ruleset_name = ruleset_obj["name"]
        target_only_rules_count = ruleset_obj["target_env_only_rules"]["count"]

        # clear ruleset first if target only not 0
        if target_only_rules_count > 0:
            result_obj = ClearRulesetTask(target_environment, country, ruleset_name).get_result_data()
            if result_obj.get(KEY_EXCEPTION) is not None:
                return

        # update ruleset
        source_xml = load_backup_applied_version_rs(rs_log_group.backup_key, ruleset_name)
        target_xml = load_backup_server_version_rs(rs_log_group.backup_key, ruleset_name)

        result_obj = UpdateRulesetTask(target_environment, country, ruleset_name,
                                       source_xml, target_xml, ruleset_obj).get_result_data()

        # add ruleset log
        rs_log_group.log(ruleset_name, RULESET_UPDATE, result_obj.get(KEY_STATUS), result_obj.get(KEY_EXCEPTION))

        if result_obj.get(KEY_STATUS) == STATUS_SUCCESS:
            sync_result_obj.updated_list.append(result_obj)
        else:
            sync_result_obj.failed_list.append(result_obj)

    return sync_result_obj


def delete_rulesets():
    pass


def send_mail(result_data, receiver=None):
    mail_sender = MailSender(config.SEND_COMPARE_RESULT_MAIL)

    # generate compare info json for mail content use
    html_content = render_to_string('ruleset_sync_result_mail_content.html', result_data)

    subject = config.SEND_COMPARE_RESULT_MAIL.get(
        "ruleset_sync_title") + " for " + result_data["country"]["name"] + " - " + result_data["source_environment"][
                  "name"] + " <> " + result_data["target_environment"]["name"]

    if receiver is None:
        mail_sender.set_receiver(config.SEND_COMPARE_RESULT_MAIL.get("receivers"))
    else:
        mail_sender.set_receiver(receiver)

    mail_sender.compose_msg(subject, None, html_content)
    mail_sender.send()
    mail_sender.quit()


class RulesetsSyncResultObject:
    def __init__(self, result_list, failed_list):
        self.result_list = result_list
        self.failed_list = failed_list


class RulesetsSyncResultListObj:
    def __init__(self):
        self.failed_list = []
        self.created_list = []
        self.updated_list = []
        self.delete_list = []
