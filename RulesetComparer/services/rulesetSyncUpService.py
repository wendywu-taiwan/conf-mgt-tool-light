from django.template.loader import render_to_string

from RulesetComparer.b2bRequestTask.downloadRulesetsTask import DownloadRulesetsTask
from RulesetComparer.b2bRequestTask.rulesetsSyncUpTask import RulesetsSyncUpTask
from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.utils.timeUtil import get_format_current_time
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


def sync_up_rulesets_without_scheduler(json_data):
    parser = CreateRulesetSyncSchedulerParser(json_data)
    for country in parser.country_list:
        result_data = sync_up_rulesets(parser, country)
        send_mail(result_data)


def get_schedulers():
    try:
        schedulers = RulesetSyncUpScheduler.objects.all()
        return schedulers
    except Exception as e:
        raise e


def create_scheduler(json_data):
    try:
        parser = CreateRulesetSyncSchedulerParser(json_data)
        sync_scheduler = RulesetSyncUpScheduler.objects.create_task(parser.source_environment_id,
                                                                    parser.target_environment_id,
                                                                    parser.module,
                                                                    parser.country_list,
                                                                    parser.action_list,
                                                                    parser.receiver_list,
                                                                    parser.interval_hour,
                                                                    parser.utc_time,
                                                                    parser.backup)
        parser.set_task_id(sync_scheduler.id)
        task = RulesetsSyncUpTask(parser)
        scheduler = CustomJobScheduler(task.listener)
        job = scheduler.add_hours_job(task.run_task, parser.interval_hour, parser.local_time)
        task.set_scheduled_job(job)
        return sync_scheduler
    except Exception as e:
        raise e


def update_scheduler(json_data):
    delete_scheduler(json_data)
    return create_scheduler(json_data)


def delete_scheduler(json_data):
    task_id = json_data.get(KEY_TASK_ID)
    RulesetSyncUpScheduler.objects.get(id=task_id).delete()


def update_scheduler_status(json_data):
    task_id = json_data.get(KEY_TASK_ID)
    enable = json_data.get(KEY_ENABLE)
    if enable:
        enable = 1
    else:
        enable = 0
    task = RulesetSyncUpScheduler.objects.update_task_status(task_id, enable)
    return task


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
    try:
        target_env_name = sync_up_pre_json[KEY_TARGET_ENV][KEY_NAME]
        country_name = sync_up_pre_json[KEY_COUNTRY][KEY_NAME]
        compare_key = sync_up_pre_json[KEY_COMPARE_HASH_KEY]
        target_env_only_rulesets = sync_up_pre_json[KEY_TARGET_ENV_ONLY_RULESETS][KEY_RULESETS_ARRAY]
        different_rulesets = sync_up_pre_json[KEY_DIFFERENT_RULESETS][KEY_RULESETS_ARRAY]
        backup_date = get_format_current_time(config.TIME_FORMAT.get("year_month_date_without_slash"))
        backup_time = get_format_current_time(config.TIME_FORMAT.get("hour_minute_second_without_slash"))

        copy_from_rulesets_folder_path = get_rule_set_path(target_env_name, country_name, compare_key)
        copy_to_rulesets_folder_path = get_ruleset_backup_path(target_env_name, country_name, backup_date + backup_time)

        info_log("backup_rulesets", "copy_from_rulesets_folder_path : " + copy_from_rulesets_folder_path)
        info_log("backup_rulesets", "copy_to_rulesets_folder_path : " + copy_to_rulesets_folder_path)

        for ruleset_obj in target_env_only_rulesets:
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), copy_from_rulesets_folder_path,
                         copy_to_rulesets_folder_path)

        for ruleset_obj in different_rulesets:
            copy_ruleset(get_file_name("_xml", ruleset_obj[KEY_NAME]), copy_from_rulesets_folder_path,
                         copy_to_rulesets_folder_path)

        # save sync pre json to backup folder
        save_auto_sync_pre_json_file(copy_to_rulesets_folder_path, sync_up_pre_json)
    except Exception as e:
        raise e


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


def sync_up_rulesets_from_backup(json_data):
    failed_rulesets_list = []
    create_rulesets_list = []
    update_rulesets_list = []
    delete_rulesets_list = []

    parser = RecoverRulesetsParser(json_data)
    environment = parser.environment
    country = parser.country
    # do delete to created rulesets
    delete_rulesets_with_backup()
    # do create to deleted rulesets
    result_obj = create_rulesets_with_backup(environment, country, parser.select_folder_name, parser.deleted_rulesets)
    failed_rulesets_list.extend(result_obj.failed_list)
    create_rulesets_list.extend(result_obj.result_list)
    # do updated to updated rulesets
    result_obj = update_rulesets_with_backup(environment, country, parser.select_folder_name, parser.updated_rulesets)
    failed_rulesets_list.extend(result_obj.failed_list)
    update_rulesets_list.extend(result_obj.result_list)

    builder = RecoverRulesetsResultBuilder(environment, country, failed_rulesets_list, create_rulesets_list,
                                           update_rulesets_list, delete_rulesets_list)

    return builder.get_data()


def create_rulesets_with_backup(environment, country, select_folder_name, rulesets):
    result_list = []
    failed_list = []
    for ruleset_name in rulesets:
        ruleset_xml = load_backup_ruleset_with_name(environment.name, country.name, select_folder_name, ruleset_name)
        result_obj = CreateRulesetTask(environment, country, ruleset_name, ruleset_xml).get_result_data()
        set_result_object(result_obj, result_list, failed_list)
    return RulesetsSyncResultObject(result_list, failed_list)


def update_rulesets_with_backup(environment, country, select_folder_name, rulesets):
    try:
        result_list = []
        failed_list = []
        if len(rulesets) == 0:
            return RulesetsSyncResultObject(result_list, failed_list)

        # download current rulesets from environment
        DownloadRulesetsTask(environment.id, country.id, rulesets, select_folder_name)
        for ruleset_name in rulesets:
            source_xml = load_backup_ruleset_with_name(environment.name, country.name, select_folder_name, ruleset_name)
            target_xml = load_server_ruleset_with_name(environment.name, country.name, select_folder_name, ruleset_name)

            # compare ruleset to know the differences
            diff_json = RulesetComparer(ruleset_name, source_xml, target_xml, is_module=False).get_data_by_builder()
            target_only_rules_count = diff_json["target_env_only_rules"][KEY_COUNT]

            if target_only_rules_count > 0:
                # clear ruleset first to remove deleted ruleset at target env
                result_obj = ClearRulesetTask(environment, country, ruleset_name).get_result_data()
                if result_obj.get("exception") is not None:
                    continue

            result_obj = UpdateRulesetTask(environment, country, ruleset_name, source_xml, target_xml,
                                           diff_json).get_result_data()
            set_result_object(result_obj, result_list, failed_list)
        return RulesetsSyncResultObject(result_list, failed_list)
    except Exception as e:
        raise e


def delete_rulesets_with_backup():
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
