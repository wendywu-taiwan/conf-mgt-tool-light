from RulesetComparer.date_model.json_builder.ruleset_log_group import RulesetLogGroupBuilder
from RulesetComparer.date_model.json_parser.get_filter_ruleset import GetFilteredRulesetParser
from RulesetComparer.date_model.json_builder.recover_filter_backup import RecoverFilterBackupObjBuilder
from RulesetComparer.models import Environment, Country, RulesetLogGroup, RulesetLog
from RulesetComparer.utils.fileManager import *


def filter_environment():
    environment_ids = RulesetLogGroup.objects.filter(
        updated__gt=0).values_list('target_environment', flat=True).order_by('target_environment').distinct()

    return list(environment_ids)


def filter_country(environment_id):
    country_ids = RulesetLogGroup.objects.filter(
        updated__gt=0, target_environment=environment_id).values_list(
        'country', flat=True).order_by('country').distinct()

    return list(country_ids)


def filter_backup_list(json_data):
    parser = GetFilteredRulesetParser(json_data)
    log_list = []
    log_group_list = []

    for log_group in parser.log_groups:
        log_group_obj = RulesetLogGroupBuilder(log_group)
        ruleset_logs = parser.get_logs_query_result(log_group_obj.backup_key)

        if ruleset_logs is None:
            continue

        log_result_obj = RecoverFilterBackupObjBuilder(log_group_obj, ruleset_logs)
        log_group_obj.update_log_count(log_result_obj.ruleset_count)

        log_list.append(log_result_obj.get_data())
        log_group_list.append(log_group_obj.get_data())

    result_data = {KEY_RULESET_LOG_GROUPS: log_group_list,
                   KEY_RULESET_LOGS: log_list}

    return result_data


def has_recovery_rulesets(env_name, country_name, date_name):
    path = get_ruleset_backup_path(env_name, country_name, date_name)
    pre_json = load_auto_sync_pre_json_file(path)
    return pre_json.get(KEY_HAS_RECOVERY_RULESETS)
