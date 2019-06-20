from django.template.loader import render_to_string

from RulesetComparer.b2bRequestTask.downloadRulesetTask import DownloadRulesetTask
from RulesetComparer.dataModel.dataObject.rulesetLogGroupObj import RulesetLogGroup, RulesetLogGroupObj
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.utils.timeUtil import get_format_current_time
from RulesetComparer.utils.rulesetLogManager import RulesetLogManager
from RulesetComparer.utils.fileManager import *
from RulesetComparer.properties.dataKey import *
from RulesetComparer.b2bRequestTask.compareRuleListTask import CompareRuleListTask
from RulesetComparer.b2bRequestTask.createRulesetTask import CreateRulesetTask
from RulesetComparer.b2bRequestTask.updateRulesetTask import UpdateRulesetTask
from RulesetComparer.b2bRequestTask.clearRulesetTask import ClearRulesetTask
from RulesetComparer.dataModel.dataParser.createRulesetSyncSchedulerParser import CreateRulesetSyncSchedulerParser
from RulesetComparer.dataModel.dataBuilder.rulesetSyncPreDataBuilder import RulesetSyncPreDataBuilder
from RulesetComparer.dataModel.dataBuilder.rulesetSyncResultDataBuilder import RulesetSyncResultDataBuilder
from RulesetComparer.dataModel.dataParser.recoverRulesetsParser import RecoverRulesetsParser
from RulesetComparer.dataModel.dataBuilder.recoverRulesetsResultBuilder import RecoverRulesetsResultBuilder
from RulesetComparer.properties.dataKey import STATUS_SUCCESS, STATUS_FAILED


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
            send_mail(result_data)
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
        sync_result_obj = create_rulesets(sync_result_obj, rs_log_group, country, parser, rulesets)
    # update rulesets
    if parser.action.update_ruleset:
        rulesets = sync_up_report_json[KEY_DIFFERENT_RULESETS][KEY_RULESETS_ARRAY]
        sync_result_obj = update_rulesets(sync_result_obj, rs_log_group, country, parser, rulesets)
    # delete rulesets
    if parser.action.delete_ruleset:
        pass
    rs_log_group.update_log_group_log_count()
    builder = RulesetSyncResultDataBuilder(sync_up_report_json, sync_result_obj)
    return builder.get_data()


# def sync_up_rulesets_from_backup(json_data):
#     try:
#         sync_result_obj = RulesetsSyncResultListObj()
#
#         parser = RecoverRulesetsParser(json_data)
#         environment = parser.environment
#         country = parser.country
#         # do delete to created rulesets
#         delete_rulesets_with_backup()
#         # do create to deleted rulesets
#         result_obj = create_rulesets_with_backup(sync_result_obj, parser)
#         # do updated to updated rulesets
#         result_obj = update_rulesets_with_backup(environment, country, parser.select_folder_name,
#                                                  parser.updated_rulesets)
#         failed_rulesets_list.extend(result_obj.failed_list)
#         update_rulesets_list.extend(result_obj.result_list)
#
#         builder = RecoverRulesetsResultBuilder(environment, country, failed_rulesets_list, create_rulesets_list,
#                                                update_rulesets_list, delete_rulesets_list)
#
#         return builder.get_data()
#     except Exception as e:
#         raise e


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

        info_log("backup rulesets", "server_rs_path : " + server_rs_path)
        info_log("backup rulesets", "source_rs_path : " + source_rs_path)
        info_log("backup rulesets", "server_rs_backup_path : " + server_rs_backup_path)
        info_log("backup rulesets", "source_rs_backup_path : " + source_rs_backup_path)

        # backup source environment only rs (it will create new ruleset to target env)
        for ruleset_obj in source_env_only_rulesets:
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), source_rs_path, source_rs_backup_path)

        # backup target environment only rs (it will be delete)
        for ruleset_obj in target_env_only_rulesets:
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), server_rs_path, server_rs_backup_path)

        # backup different ruleset in both env
        for ruleset_obj in different_rulesets:
            # backup rs on server version
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), server_rs_path, server_rs_backup_path)
            # backup rs will be applied to server version
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), source_rs_path, source_rs_backup_path)

        # save sync pre json to backup folder
        # save_auto_sync_pre_json_file(get_ruleset_backup_path(None, None, None), sync_up_pre_json)
    except Exception as e:
        raise e


def create_rulesets(sync_result_obj, rs_log_group, country, parser, rulesets):
    if len(rulesets) == 0:
        return sync_result_obj

    for ruleset_obj in rulesets:
        ruleset_name = ruleset_obj["name"]
        ruleset_xml = load_backup_applied_version_rs(rs_log_group.backup_key, ruleset_name)

        result_obj = CreateRulesetTask(parser.target_environment, country, ruleset_name, ruleset_xml).get_result_data()

        # add ruleset log
        rs_log_group.log(ruleset_name,RULESET_CREATE,result_obj.get(KEY_STATUS),result_obj.get(KEY_EXCEPTION))

        if result_obj.get(KEY_STATUS) == STATUS_SUCCESS:
            sync_result_obj.created_list.append(result_obj)
        else:
            sync_result_obj.failed_list.append(result_obj)

    return sync_result_obj


def update_rulesets(sync_result_obj, rs_log_group, country, parser, rulesets):
    for ruleset_obj in rulesets:
        ruleset_name = ruleset_obj["name"]
        target_only_rules_count = ruleset_obj["target_env_only_rules"]["count"]

        # clear ruleset first if target only not 0
        if target_only_rules_count > 0:
            result_obj = ClearRulesetTask(parser.target_environment, country, ruleset_name).get_result_data()
            if result_obj.get(KEY_EXCEPTION) is not None:
                return

        # update ruleset
        source_xml = load_backup_applied_version_rs(rs_log_group.backup_key, ruleset_name)
        target_xml = load_backup_server_version_rs(rs_log_group.backup_key, ruleset_name)

        result_obj = UpdateRulesetTask(parser.target_environment, country, ruleset_name,
                                       source_xml, target_xml, ruleset_obj).get_result_data()

        # add ruleset log
        rs_log_group.log(ruleset_name, RULESET_CREATE, result_obj.get(KEY_STATUS), result_obj.get(KEY_EXCEPTION))

        if result_obj.get(KEY_STATUS) == STATUS_SUCCESS:
            sync_result_obj.updated_list.append(result_obj)
        else:
            sync_result_obj.failed_list.append(result_obj)

    return sync_result_obj


def delete_rulesets():
    pass


# def create_rulesets_with_backup(sync_result_obj, parser):
#     for ruleset_name in parser.deleted_rulesets:
#         ruleset_xml = load_backup_ruleset_with_name(parser.environment.name, parser.country.name,
#                                                     parser.select_folder_name, ruleset_name)
#
#         create_ruleset(sync_result_obj, parser.backup_key, ruleset_name, ruleset_xml,
#                        parser.environment, parser.country)
#
#     return sync_result_obj
#
#
# def create_ruleset(sync_result_obj, backup_key, ruleset_name, ruleset_xml, environment, country):
#     result_obj = CreateRulesetTask(environment, country, ruleset_name, ruleset_xml).get_result_data()
#
#     # add ruleset log
#     RulesetLogManager.add_ruleset_log(backup_key,
#                                       RULESET_CREATE,
#                                       result_obj[KEY_STATUS],
#                                       ruleset_name,
#                                       result_obj[KEY_EXCEPTION])
#
#     if result_obj.get(KEY_STATUS) == STATUS_SUCCESS:
#         sync_result_obj.created_list.append(result_obj)
#     else:
#         sync_result_obj.failed_list.append(result_obj)
#
#     return result_obj

# def update_rulesets_with_backup(environment, country, select_folder_name, rulesets):
#     try:
#         result_list = []
#         failed_list = []
#         if len(rulesets) == 0:
#             return RulesetsSyncResultObject(result_list, failed_list)
#
#         for ruleset_name in rulesets:
#             task = DownloadRulesetTask(environment.id, country.id, ruleset_name)
#
#             # check download ruleset success or fail
#             if not check_result_success(task.get_result_data(), failed_list):
#                 continue
#
#             target_xml = task.get_ruleset_xml()
#             source_xml = load_backup_ruleset_with_name(environment.name, country.name, select_folder_name, ruleset_name)
#
#             # compare ruleset to know the differences
#             diff_json = RulesetComparer(ruleset_name, source_xml, target_xml, is_module=False).get_data_by_builder()
#             target_only_rules_count = diff_json["target_env_only_rules"][KEY_COUNT]
#
#             if target_only_rules_count > 0:
#                 # clear ruleset first to remove deleted ruleset at target env
#                 result_obj = ClearRulesetTask(environment, country, ruleset_name).get_result_data()
#
#                 if not check_result_success(result_obj, failed_list):
#                     continue
#
#             result_obj = UpdateRulesetTask(environment, country, ruleset_name, source_xml, target_xml,
#                                            diff_json).get_result_data()
#             check_result_success(result_obj, failed_list, result_list)
#
#         return RulesetsSyncResultObject(result_list, failed_list)
#     except Exception as e:
#         raise e


def delete_rulesets_with_backup():
    pass


def send_mail(result_data):
    mail_sender = MailSender(config.SEND_COMPARE_RESULT_MAIL)

    # generate compare info json for mail content use
    html_content = render_to_string('ruleset_sync_result_mail_content.html', result_data)

    subject = config.SEND_COMPARE_RESULT_MAIL.get(
        "ruleset_sync_title") + " for " + result_data["country"]["name"] + " - " + result_data["source_environment"][
                  "name"] + " <> " + result_data["target_environment"]["name"]

    mail_sender.set_receiver(config.SEND_COMPARE_RESULT_MAIL.get("receivers"))
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
