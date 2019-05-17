import traceback
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.models import Environment, Country, RulesetSyncUpScheduler
from RulesetComparer.b2bRequestTask.downloadRulesetsTask import DownloadRulesetsTask
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.b2bRequestTask.compareRuleListTask import CompareRuleListTask
from RulesetComparer.b2bRequestTask.dailyCompareReportTask import DailyCompareReportTask
from RulesetComparer.b2bRequestTask.packedRulesetsTask import PackedRulesetsTask
from RulesetComparer.b2bRequestTask.clearRulesetFilesTask import ClearRulesetFilesTask

from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.dataModel.dataParser.getFilteredRulesetParser import GetFilteredRulesetParser
from RulesetComparer.dataModel.dataParser.dbReportSchedulerParser import DBReportSchedulerParser
from RulesetComparer.dataModel.dataParser.createReportSchedulerTaskParser import CreateReportSchedulerTaskParser
from RulesetComparer.dataModel.dataParser.downloadRulesetParser import DownloadRulesetParser

from RulesetComparer.models import ReportSchedulerInfo
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils import rulesetUtil, fileManager, stringFilter
from RulesetComparer.dataModel.xml.ruleSetObject import RulesetObject as ParseRuleModel
from RulesetComparer.serializers.serializers import RuleSerializer
from RulesetComparer.properties import dataKey
from RulesetComparer.services import rulesetSyncUpService
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


def create_report_scheduler(json_data):
    try:
        parser = CreateReportSchedulerTaskParser(json_data)
        report_scheduler = ReportSchedulerInfo.objects.create_task(parser.base_env_id,
                                                                   parser.compare_env_id,
                                                                   parser.module_id,
                                                                   parser.country_list,
                                                                   parser.mail_content_type_list,
                                                                   parser.mail_list,
                                                                   parser.interval_hour,
                                                                   parser.utc_time)

        parser.task_id = report_scheduler.id
        run_report_scheduler(parser)
        return report_scheduler
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def update_report_scheduler(json_data):
    try:
        parser = CreateReportSchedulerTaskParser(json_data)
        report_scheduler = ReportSchedulerInfo.objects.update_task(parser.task_id,
                                                                   parser.base_env_id,
                                                                   parser.compare_env_id,
                                                                   parser.country_list,
                                                                   parser.mail_content_type_list,
                                                                   parser.mail_list,
                                                                   parser.interval_hour,
                                                                   parser.utc_time)
        run_report_scheduler(parser)
        return report_scheduler
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def delete_scheduler(task_id):
    try:
        ReportSchedulerInfo.objects.filter(id=task_id).delete()
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def run_report_scheduler(parser):
    daily_task = DailyCompareReportTask(parser)
    scheduler = CustomJobScheduler(daily_task.scheduler_listener)
    job = scheduler.add_hours_job(daily_task.run_task, parser.interval_hour, parser.local_time)
    ReportSchedulerInfo.objects.update_job_id(parser.task_id, job.id)
    daily_task.set_scheduled_job(job)


def restart_all_scheduler():
    try:
        # clear zip and ruleset file scheduler
        clear_ruleset_task = ClearRulesetFilesTask()
        scheduler = CustomJobScheduler(clear_ruleset_task.scheduler_listener)
        job = scheduler.add_hours_job_now(clear_ruleset_task.run_task, 24)
        clear_ruleset_task.set_scheduled_job(job)

        info_log(None, "restart all scheduler")
        if len(ReportSchedulerInfo.objects.all()) > 0:
            scheduler_model_list = ReportSchedulerInfo.objects.all()
            # report scheduler
            for scheduler in scheduler_model_list:
                country_list = scheduler.country_list.values(KEY_ID)
                mail_content_type_list = scheduler.mail_content_type_list.values(KEY_ID)
                parser = DBReportSchedulerParser(scheduler, country_list, mail_content_type_list)
                ReportSchedulerInfo.objects.update_next_proceed_time(parser.task_id, parser.utc_time)
                run_report_scheduler(parser)

        rulesetSyncUpService.restart_schedulers()

        info_log(None, "restart all scheduler success")
    except BaseException as e:
        error_log(traceback.format_exc())
        raise e
