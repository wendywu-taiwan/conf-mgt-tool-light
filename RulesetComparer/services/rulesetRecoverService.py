from RulesetComparer.dataModel.dataParser.getFilteredRulesetParser import GetFilteredRulesetParser
from RulesetComparer.dataModel.dataParser.diffBackupRulesetParser import DiffBackupRulesetParser
from RulesetComparer.dataModel.dataBuilder.recoverFilterBackupObjBuilder import RecoverFilterBackupObjBuilder
from RulesetComparer.dataModel.dataBuilder.recoverFilterObjBuilder import RecoverFilterObjBuilder
from RulesetComparer.dataModel.dataBuilder.diffRulesetPageBuilder import DiffRulesetPageBuilder
from RulesetComparer.models import Environment, Country
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.fileManager import *


def filter_backup_list(json_data):
    parser = GetFilteredRulesetParser(json_data)
    backup_date_folder_path = get_ruleset_backup_path(parser.environment.name,
                                                      parser.country.name,
                                                      "")
    date_folder_names = get_files_list_in_path(backup_date_folder_path)
    backup_ruleset_objects = []
    for date_folder_name in date_folder_names:
        backup_ruleset_path = get_ruleset_backup_path(parser.environment.name,
                                                      parser.country.name,
                                                      date_folder_name)
        pre_json = load_auto_sync_pre_json_file(backup_ruleset_path)
        backup_ruleset_object = RecoverFilterBackupObjBuilder(date_folder_name, pre_json, parser.filter_keys)
        if backup_ruleset_object.has_filter_keys:
            backup_ruleset_objects.append(backup_ruleset_object.get_data())

    result_data = RecoverFilterObjBuilder(parser.country, parser.environment, backup_ruleset_objects).get_data()
    return result_data


def filter_environment():
    backup_folder_path = get_ruleset_backup_path("", "", "")
    environment_name_list = get_files_list_in_path(backup_folder_path, "__init__.py")
    environment_list = []
    for environment_name in environment_name_list:
        environment = Environment.objects.get(name=environment_name)
        environment_list.append(environment)

    return environment_list


def filter_country(environment_id):
    environment = Environment.objects.get(id=environment_id)
    backup_env_folder_path = get_ruleset_backup_path(environment.name, "", "")
    country_name_list = get_files_list_in_path(backup_env_folder_path, "__init__.py")

    country_list = []
    for country_name in country_name_list:
        country = Country.objects.get(name=country_name)
        country_list.append(country)
    return country_list


def diff_backup_ruleset(json_data):
    parser = DiffBackupRulesetParser(json_data)
    comparer = RulesetComparer(parser.ruleset_name, parser.backup_ruleset_xml, parser.server_ruleset_xml, False)
    builder = DiffRulesetPageBuilder(parser.ruleset_name, KEY_BACKUP, parser.environment.name, comparer.get_diff_data())
    return builder.get_data()
