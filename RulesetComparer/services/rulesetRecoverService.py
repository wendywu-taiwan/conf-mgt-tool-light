from RulesetComparer.dataModel.dataBuilder.rulesetLogGroupBuilder import RulesetLogGroupBuilder
from RulesetComparer.dataModel.dataParser.getFilteredRulesetParser import GetFilteredRulesetParser
from RulesetComparer.dataModel.dataParser.diffBackupRulesetParser import DiffBackupRulesetParser
from RulesetComparer.dataModel.dataBuilder.recoverFilterBackupObjBuilder import RecoverFilterBackupObjBuilder
from RulesetComparer.dataModel.dataBuilder.recoverFilterObjBuilder import RecoverFilterObjBuilder
from RulesetComparer.dataModel.dataBuilder.diffRulesetPageBuilder import DiffRulesetPageBuilder
from RulesetComparer.models import Environment, Country, RulesetLogGroup, RulesetLog
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.fileManager import *


def filter_environment():
    environment_list = []
    environment_ids = RulesetLogGroup.objects.filter(log_count__gt=0).values_list('target_environment',
                                                                                  flat=True).order_by(
        'target_environment').distinct()

    for env_id in environment_ids:
        environment = Environment.objects.get(id=env_id)
        environment_list.append(environment)

    return environment_list


def filter_country(environment_id):
    country_list = []
    country_ids = RulesetLogGroup.objects.filter(log_count__gt=0, target_environment=environment_id).values_list(
        'country', flat=True).order_by('country').distinct()

    for country_id in country_ids:
        country = Country.objects.get(id=country_id)
        country_list.append(country)

    return country_list


def filter_backup_list(json_data):
    parser = GetFilteredRulesetParser(json_data)
    log_list = []
    log_group_list = []
    ruleset_log_groups = RulesetLogGroup.objects.filter(log_count__gt=0, target_environment=parser.environment.id,
                                                        country=parser.country.id).values().order_by('-update_time').distinct()

    for obj in ruleset_log_groups:
        log_group_obj = RulesetLogGroupBuilder(obj)
        pre_json = load_auto_sync_pre_json_file(get_sync_pre_data_path(obj.get(KEY_BACKUP_KEY)))
        log_result_obj = RecoverFilterBackupObjBuilder(pre_json,
                                                       log_group_obj.update_time,
                                                       log_group_obj.backup_key,
                                                       parser.filter_keys)

        log_group_obj.update_log_count(log_result_obj.log_count)

        if log_result_obj.has_filtered_rulesets is True:
            log_list.append(log_result_obj.get_data())
            log_group_list.append(log_group_obj.get_data())

    result_data = {KEY_RULESET_LOG_GROUPS: log_group_list,
                   KEY_RULESET_LOGS: log_list}

    return result_data


def diff_backup_ruleset(json_data):
    parser = DiffBackupRulesetParser(json_data)
    comparer = RulesetComparer(parser.ruleset_name, parser.backup_ruleset_xml, parser.server_ruleset_xml, False)
    builder = DiffRulesetPageBuilder(parser.ruleset_name, KEY_BACKUP, parser.environment.name, comparer.get_diff_data())
    return builder.get_data()


def has_recovery_rulesets(env_name, country_name, date_name):
    path = get_ruleset_backup_path(env_name, country_name, date_name)
    pre_json = load_auto_sync_pre_json_file(path)
    return pre_json.get(KEY_HAS_RECOVERY_RULESETS)
