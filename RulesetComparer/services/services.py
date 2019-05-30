import traceback

from RulesetComparer.b2bRequestTask.downloadRulesetTask import DownloadRulesetTask
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.b2bRequestTask.downloadRulesetsTask import DownloadRulesetsTask
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.b2bRequestTask.compareRuleListTask import CompareRuleListTask
from RulesetComparer.b2bRequestTask.packedRulesetsTask import PackedRulesetsTask
from RulesetComparer.b2bRequestTask.clearRulesetFilesTask import ClearRulesetFilesTask
from RulesetComparer.b2bRequestTask.clearCompareReportFilesTask import ClearCompareReportFilesTask
from RulesetComparer.b2bRequestTask.clearRulesetArchivedFilesTask import ClearRulesetArchivedFilesTask

from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.dataModel.dataParser.getFilteredRulesetParser import GetFilteredRulesetParser
from RulesetComparer.dataModel.dataParser.downloadRulesetParser import DownloadRulesetParser

from RulesetComparer.utils import rulesetUtil, fileManager, stringFilter
from RulesetComparer.services import rulesetSyncService, rulesetSyncSchedulerService, rulesetReportSchedulerService
from django.template.loader import get_template

from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.rulesetUtil import load_server_ruleset_with_name


def get_rule_list_from_b2b(environment, country):
    task = DownloadRuleListTask(environment, country)
    return task


def compare_rule_list_rule_set(base_env_id, compare_env_id, country_id):
    task = CompareRuleListTask(base_env_id, compare_env_id, country_id)
    return task


def compare_ruleset_test():
    try:
        ruleset_name = "RS_KR_PROCESS"
        # source_xml = load_git_ruleset_with_name("TW", ruleset_name)
        source_xml = load_server_ruleset_with_name("PROD", "KR", 111111111, ruleset_name)
        target_xml = load_server_ruleset_with_name("GIT", "KR", 111111111, ruleset_name)

        diff_json = RulesetComparer(ruleset_name, source_xml, target_xml, is_module=False).get_data_by_builder()
        # source_xml = DownloadRulesetTask(base_env_id, country_id, ruleset_name).get_ruleset_xml()
        # compared_xml = DownloadRulesetTask(compare_env_id, country_id, ruleset_name).get_ruleset_xml()
        # ruleset_name = "RS_TW_COPY_INTO_EXISTING_CASE_TOOLBAR"

    except Exception as e:
        raise e


def generate_compare_report(compare_key):
    data = fileManager.load_compare_result_file(compare_key)
    template = get_template("compare_result_report.html")
    html = template.render(data)
    fileManager.save_compare_result_html(compare_key, html)


def get_filtered_ruleset_list(json_data):
    try:
        parser = GetFilteredRulesetParser(json_data)
        if parser.is_git:
            git_file_path = get_rule_set_git_path(parser.country.name)
            rule_name_list = fileManager.get_rule_name_list(git_file_path)
        else:
            task = DownloadRuleListTask(parser.environment.id,
                                        parser.country.id)
            rule_name_list = task.get_result_data()

        filter_name_list = stringFilter.array_filter(rule_name_list, parser.filter_keys)
        return filter_name_list
    except Exception:
        error_log(traceback.format_exc())
        return traceback.print_exc()


def download_rulesets(json_data):
    try:
        parser = DownloadRulesetParser(json_data)

        if parser.environment.name == GIT.get("environment_name"):
            # update git to latest code
            manager = GitManager(get_ruleset_git_root_path(), settings.GIT_BRANCH_DEVELOP)
            manager.pull()
            resource_path = get_rule_set_git_path(parser.country.name)
        else:
            if parser.ruleset_exist is False:
                task = DownloadRulesetsTask(parser.environment.id, parser.country.id, parser.rule_name_list,
                                            parser.compare_hash_key)
            resource_path = get_rule_set_path(parser.environment.name, parser.country.name, parser.compare_hash_key)

        copied_path = get_rule_set_path(parser.environment.name, parser.country.name, parser.compare_hash_key * 2)
        task = PackedRulesetsTask(parser.rule_name_xml_list, resource_path, copied_path)
        return task.zip_file
    except Exception:
        error_log(traceback.format_exc())


def restart_all_scheduler():
    try:
        # clear zip and ruleset file scheduler
        clear_zip_ruleset_task = ClearRulesetArchivedFilesTask()
        clear_ruleset_task = ClearRulesetFilesTask()
        clear_compare_report_task = ClearCompareReportFilesTask()

        scheduler = CustomJobScheduler()
        scheduler.add_hours_job_now(clear_ruleset_task.run_task, 24)
        scheduler.add_hours_job_now(clear_zip_ruleset_task.run_task, 24)
        scheduler.add_hours_job_now(clear_compare_report_task.run_task, 24)

        info_log(None, "restart all scheduler")
        rulesetReportSchedulerService.restart_schedulers()
        rulesetSyncSchedulerService.restart_schedulers()

        info_log(None, "restart all scheduler success")
    except BaseException as e:
        error_log(traceback.format_exc())
        raise e
