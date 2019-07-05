import traceback

from RulesetComparer.dataModel.dataBuilder.rulesetDetailBuilder import RulesetDetailBuilder
from RulesetComparer.dataModel.rulesetLoader.gitRulesetLoader import GitRulesetLoader
from RulesetComparer.dataModel.rulesetLoader.serverRulesetLoader import ServerRulesetLoader
from RulesetComparer.dataModel.rulesetLoader.backupRulesetLoader import BackupRulesetLoader
from RulesetComparer.models import Environment
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


def get_rule_list_from_b2b(environment, country):
    task = DownloadRuleListTask(environment, country)
    return task


def compare_rule_list_rule_set(base_env_id, compare_env_id, country_id):
    task = CompareRuleListTask(base_env_id, compare_env_id, country_id)
    return task


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


def ruleset_detail_page_data(environment_id, country_id, compare_key, ruleset_name):
    environment = Environment.objects.get(id=environment_id)
    if environment.name == GIT_NAME:
        ruleset_loader = GitRulesetLoader(country_id, ruleset_name, False)
    else:
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
