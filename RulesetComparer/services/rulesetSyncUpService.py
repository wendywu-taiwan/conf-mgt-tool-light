from django.template.loader import render_to_string

from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.properties.dataKey import *
from RulesetComparer.b2bRequestTask.compareRuleListTask import CompareRuleListTask
from RulesetComparer.b2bRequestTask.createRulesetTask import CreateRulesetTask
from RulesetComparer.b2bRequestTask.updateRulesetTask import UpdateRulesetTask
from RulesetComparer.b2bRequestTask.clearRulesetTask import ClearRulesetTask
from RulesetComparer.dataModel.dataParser.createRulesetSyncSchedulerParser import CreateRulesetSyncSchedulerParser
from RulesetComparer.dataModel.dataBuilder.rulesetSyncPreDataBuilder import RulesetSyncPreDataBuilder
from RulesetComparer.dataModel.dataBuilder.rulesetSyncResultDataBuilder import RulesetSyncResultDataBuilder
from RulesetComparer.models import RulesetSyncUpScheduler
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


def sync_up_rulesets_test(json_data):
    parser = CreateRulesetSyncSchedulerParser(json_data)
    for country in parser.country_list:
        result_data = sync_up_rulesets(parser, country)
        send_mail(result_data)


def create_scheduler(json_data):
    try:
        parser = CreateRulesetSyncSchedulerParser(json_data)
        info_model = RulesetSyncUpScheduler.objects.create_task(parser.source_environment_id,
                                                                parser.target_environment_id,
                                                                parser.module_id,
                                                                parser.country_list,
                                                                parser.action_list,
                                                                parser.receiver_list,
                                                                parser.interval_hour,
                                                                parser.utc_time,
                                                                parser.backup)
        sync_up_rulesets(parser)
        return info_model
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def update_scheduler(json_data):
    pass


def sync_up_rulesets(parser, country):
    compare_report_json = CompareRuleListTask(parser.source_environment_id, parser.target_environment_id,
                                              country.id).get_report()
    sync_up_report_json = RulesetSyncPreDataBuilder(compare_report_json).get_data()

    if sync_up_report_json is None:
        raise Exception("can not generate ruleset sync pre data")

    if parser.backup:
        backup_rulesets(sync_up_report_json)

    failed_rulesets_list = []
    create_rulesets_list = []
    update_rulesets_list = []
    delete_rulesets_list = []

    if parser.action.create_ruleset:
        result_obj = create_rulesets(country, parser, sync_up_report_json)
        failed_rulesets_list.extend(result_obj.failed_list)
        create_rulesets_list.extend(result_obj.result_list)

    if parser.action.update_ruleset:
        result_obj = update_rulesets(country, parser, sync_up_report_json)
        failed_rulesets_list.extend(result_obj.failed_list)
        update_rulesets_list.extend(result_obj.result_list)

    if parser.action.delete_ruleset:
        pass

    builder = RulesetSyncResultDataBuilder(sync_up_report_json, failed_rulesets_list,
                                           create_rulesets_list, update_rulesets_list,
                                           delete_rulesets_list)

    return builder.get_data()


def backup_rulesets(sync_up_pre_json):
    target_env_name = sync_up_pre_json[KEY_TARGET_ENV][KEY_NAME]
    country_name = sync_up_pre_json[KEY_COUNTRY][KEY_NAME]
    compare_key = sync_up_pre_json[KEY_COMPARE_HASH_KEY]
    target_env_only_rulesets = sync_up_pre_json[KEY_TARGET_ENV_ONLY_RULESETS][KEY_RULESETS_ARRAY]
    different_rulesets = sync_up_pre_json[KEY_DIFFERENT_RULESETS][KEY_RULESETS_ARRAY]
    backup_date = get_format_current_time(config.TIME_FORMAT.get("year_month_date_without_slash"))

    copy_from_rulesets_folder_path = get_rule_set_path(target_env_name, country_name, compare_key)
    copy_to_rulesets_folder_path = get_ruleset_backup_path(target_env_name, country_name, backup_date)

    info_log("backup_rulesets", "copy_from_rulesets_folder_path : " + copy_from_rulesets_folder_path)
    info_log("backup_rulesets", "copy_to_rulesets_folder_path : " + copy_to_rulesets_folder_path)

    for ruleset_obj in target_env_only_rulesets:
        copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]),
                     copy_from_rulesets_folder_path, copy_to_rulesets_folder_path)

    for ruleset_obj in different_rulesets:
        copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]),
                     copy_from_rulesets_folder_path, copy_to_rulesets_folder_path)


def create_rulesets(country, parser, sync_up_report_json):
    rulesets = sync_up_report_json["source_env_only_rulesets"]["rulesets_array"]
    result_list = []
    failed_list = []

    if len(rulesets) == 0:
        return RulesetsSyncResultObject(result_list, failed_list)

    for ruleset_obj in rulesets:
        ruleset_name = ruleset_obj["name"]
        ruleset_xml = load_ruleset_with_name(ruleset_name, parser.source_environment.name,
                                             country.name, sync_up_report_json[COMPARE_RULE_COMPARE_HASH_KEY])

        result_obj = CreateRulesetTask(parser.target_environment, country, ruleset_name, ruleset_xml).get_result_data()
        set_result_object(result_obj, result_list, failed_list)
    return RulesetsSyncResultObject(result_list, failed_list)


def update_rulesets(country, parser, sync_up_report_json):
    rulesets = sync_up_report_json["different_rulesets"]["rulesets_array"]
    result_list = []
    failed_list = []
    if len(rulesets) == 0:
        return RulesetsSyncResultObject(result_list, failed_list)

    for ruleset_obj in rulesets:
        ruleset_name = ruleset_obj["name"]
        target_only_rules_count = ruleset_obj["target_env_only_rules"]["count"]

        if target_only_rules_count > 0:
            # clear ruleset first to remove deleted ruleset at target env
            result_obj = ClearRulesetTask(parser.target_environment, country, ruleset_name).get_result_data()

            if result_obj.get("exception") is not None:
                return

        compare_hash_key = sync_up_report_json[COMPARE_RULE_COMPARE_HASH_KEY]
        source_xml = load_ruleset_with_name(ruleset_name, parser.source_environment.name,
                                            country.name, compare_hash_key)
        target_xml = load_ruleset_with_name(ruleset_name, parser.target_environment.name,
                                            country.name, compare_hash_key)

        result_obj = UpdateRulesetTask(parser.target_environment, country, ruleset_name, source_xml, target_xml,
                                       ruleset_obj).get_result_data()
        set_result_object(result_obj, result_list, failed_list)
    return RulesetsSyncResultObject(result_list, failed_list)


def delete_rulesets():
    pass


def set_result_object(result_obj, result_list, failed_list):
    if result_obj.get("status") == STATUS_SUCCESS:
        result_list.append(result_obj)
    else:
        failed_list.append(result_obj)


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
