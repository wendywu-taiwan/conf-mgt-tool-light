import traceback
from RulesetComparer.utils import rulesetUtil
from RulesetComparer.date_model.json_builder.compare_ruleset_list_page import CompareRulesetListPageBuilder
from RulesetComparer.task.download_ruleset import DownloadRulesetTask
from RulesetComparer.date_model.json_builder.diff_ruleset_page import DiffRulesetPageBuilder
from RulesetComparer.date_model.json_builder.ruleset_detail_page import RulesetDetailBuilder
from RulesetComparer.date_model.json_builder.filter_ruleset_download_page import FilterRulesetDownloadPageBuilder
from RulesetComparer.date_model.ruleset_loader.git import GitRulesetLoader
from RulesetComparer.date_model.ruleset_loader.server import ServerRulesetLoader
from RulesetComparer.date_model.ruleset_loader.backup import BackupRulesetLoader
from RulesetComparer.models import Environment
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_parser.ruleset_diff_backup import RulesetDiffBackupParser
from RulesetComparer.date_model.json_parser.ruleset_diff_backup_with_server import RulesetDiffBackupWithServerParser
from RulesetComparer.date_model.json_parser.ruleset_diff_result import RulesetDiffCompareResultParser
from RulesetComparer.task.download_ruleset_list import DownloadRuleListTask
from RulesetComparer.task.compare_ruleset_list import CompareRuleListTask
from RulesetComparer.task.packed_rulesets import PackedRulesetsTask
from RulesetComparer.task.clear_ruleset_files import ClearRulesetFilesTask
from RulesetComparer.task.clear_report_files import ClearCompareReportFilesTask
from RulesetComparer.task.clear_ruleset_zip_files import ClearRulesetArchivedFilesTask

from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.date_model.json_parser.get_filter_ruleset import GetFilteredRulesetParser
from RulesetComparer.date_model.json_parser.download_ruleset import DownloadRulesetParser

from RulesetComparer.utils import fileManager
from RulesetComparer.services import sync_scheduler, report_scheduler
from django.template.loader import get_template

from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.date_model.json_builder.server_log_page import ServerLogPageBuilder
from common.services.git_manage_services import get_ruleset_git_path, get_ruleset_git_country_path


def server_log_page(user, log_type):
    data = ServerLogPageBuilder(user, log_type).get_data()
    return data


def get_rule_list_from_b2b(environment, country):
    task = DownloadRuleListTask(environment, country)
    return task


def compare_rule_list_rule_set(base_env_id, compare_env_id, country_id):
    task = CompareRuleListTask(base_env_id, compare_env_id, country_id)
    result_data = fileManager.load_compare_result_file(task.compare_hash_key)
    data = CompareRulesetListPageBuilder(result_data).get_data()

    return data


def compare_ruleset_test():
    try:
        pass
    except Exception as e:
        raise e


def generate_compare_report(compare_key):
    data = fileManager.load_compare_result_file(compare_key)
    template = get_template("compare_result_report.html")
    html = template.render(data)
    fileManager.save_compare_result_html(compare_key, html)


def get_filtered_ruleset_page_data(json_data):
    parser = GetFilteredRulesetParser(json_data)

    if parser.is_git:
        git_file_path = get_ruleset_git_country_path(parser.country.name)
        rule_name_list = fileManager.get_rule_name_list(git_file_path)
    else:
        task = DownloadRuleListTask(parser.environment.id, parser.country.id)
        rule_name_list = task.get_result_data()

    builder = FilterRulesetDownloadPageBuilder(parser.country, parser.environment,
                                               parser.filter_keys, rule_name_list)
    return builder.get_data()


def ruleset_detail_page_data(environment_id, country_id, ruleset_name, compare_key=None):
    environment = Environment.objects.get(id=environment_id)
    if environment.name == GIT_NAME:
        ruleset_loader = GitRulesetLoader(country_id, ruleset_name, False)
    else:
        if compare_key is None:
            compare_key = DownloadRulesetTask(environment_id, country_id, ruleset_name).compare_hash_key

        ruleset_loader = ServerRulesetLoader(compare_key, environment_id,
                                             country_id, ruleset_name)
    return RulesetDetailBuilder(ruleset_loader).get_data()


def ruleset_detail_backup_page_data(backup_key, backup_folder, ruleset_name):
    ruleset_loader = BackupRulesetLoader(backup_key, backup_folder, ruleset_name)
    return RulesetDetailBuilder(ruleset_loader).get_data()


def download_rulesets(json_data):
    try:
        parser = DownloadRulesetParser(json_data)
        copied_key = hash(timeUtil.get_current_timestamp())
        resource_path = parser.ruleset_resource_path
        copied_path = get_rule_set_path(parser.environment.name, parser.country.name, copied_key)
        task = PackedRulesetsTask(parser.rule_name_xml_list, resource_path, copied_path)
        return task.zip_file
    except Exception:
        error_log(traceback.format_exc())


# open diff page with compare result data
def ruleset_diff_compare_result(compare_key, ruleset_name):
    result_data = fileManager.load_compare_result_file(compare_key)
    parser = RulesetDiffCompareResultParser(result_data, ruleset_name)
    builder = DiffRulesetPageBuilder(parser.ruleset_name, parser.source_environment.name,
                                     parser.target_environment.name, parser.ruleset_diff_data)
    return builder.get_data()


# open diff page with two backup rulesets compare data
def ruleset_diff_backup(backup_key, ruleset_name):
    parser = RulesetDiffBackupParser(backup_key, ruleset_name)
    comparer = RulesetComparer(parser.ruleset_name, parser.source_ruleset_xml, parser.target_ruleset_xml, False)
    builder = DiffRulesetPageBuilder(parser.ruleset_name, parser.source_environment.name,
                                     parser.target_environment.name, comparer.get_diff_data())
    return builder.get_data()


# open diff page with backup ruleset compare with server ruleset data
def ruleset_diff_backup_with_server(backup_key, backup_folder, ruleset_name):
    parser = RulesetDiffBackupWithServerParser(backup_key, backup_folder, ruleset_name)
    comparer = RulesetComparer(parser.ruleset_name, parser.backup_ruleset_xml, parser.server_ruleset_xml, False)
    builder = DiffRulesetPageBuilder(parser.ruleset_name, BACKUP_ENVIRONMENT_NAME, parser.environment.name,
                                     comparer.get_diff_data())
    return builder.get_data()


def ruleset_diff_test():
    try:
        compare_hash_key = "123456789"
        ruleset_name = "RS_KR_DG_DC"
        base_ruleset_object = rulesetUtil.load_ruleset_object(ruleset_name, "KR", "GIT", compare_hash_key)
        compare_ruleset_object = rulesetUtil.load_ruleset_object(ruleset_name, "KR", "INT1", compare_hash_key)
        comparer = RulesetComparer(ruleset_name, base_ruleset_object, compare_ruleset_object, is_module=True)
        diff_data = comparer.get_diff_data()
        info_log("ruleset_diff_test", "diff data:" + diff_data)
    except Exception as e:
        traceback.format_exc()
