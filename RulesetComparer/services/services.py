import traceback
from RulesetComparer.utils.logger import *
from RulesetComparer.b2bRequestTask.downloadRuleSetTask import DownloadRuleSetTask
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.b2bRequestTask.compareRuleListTask import CompareRuleListTask
from RulesetComparer.b2bRequestTask.dailyCompareReportTask import DailyCompareReportTask

from RulesetComparer.utils.sendMailScheduler import SendMailScheduler
from RulesetComparer.dataModel.dataParser.dbReportSchedulerParser import DBReportSchedulerParser
from RulesetComparer.dataModel.dataBuilder.reportSchedulerInfoBuilder import ReportSchedulerInfoBuilder
from RulesetComparer.dataModel.dataParser.createReportSchedulerTaskParser import CreateReportSchedulerTaskParser
from RulesetComparer.dataModel.dataParser.updateReportSchedularTaskParser import UpdateReportSchedulerTaskParser

from RulesetComparer.models import ReportSchedulerInfo
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils import rulesetUtil, fileManager
from RulesetComparer.dataModel.xml.ruleSetParser import RulesModel as ParseRuleModel
from RulesetComparer.serializers.serializers import RuleSerializer
from RulesetComparer.properties import dataKey
from django.template.loader import get_template


def get_rule_list_from_b2b(environment, country):
    task = DownloadRuleListTask(environment, country)
    return task


def get_rule_from_b2b(environment, country, rule_set_name):
    task = DownloadRuleSetTask(environment, country, rule_set_name)

    ruleset = task.get_rule_set_file()
    rules_model = ParseRuleModel(ruleset)
    rule_data = RuleSerializer(rules_model.get_rules_data_array())
    return rule_data


def compare_rule_list_rule_set(base_env_id, compare_env_id, country_id):
    task = CompareRuleListTask(base_env_id, compare_env_id, country_id)
    return task


def generate_compare_report(compare_key):
    data = fileManager.load_compare_result_file(compare_key)
    template = get_template("compare_result_report.html")
    html = template.render(data)
    fileManager.save_compare_result_html(compare_key, html)


def diff_rule_set(base_env_id, compare_env_id, country_id, compare_key, rule_set_name):
    base_rule = rulesetUtil.load_rule_file_with_id(base_env_id, country_id,
                                                   compare_key, rule_set_name)
    compare_rule = rulesetUtil.load_rule_file_with_id(compare_env_id, country_id,
                                                      compare_key, rule_set_name)

    base_module = ParseRuleModel(base_rule)
    compare_module = ParseRuleModel(compare_rule)

    comparer = RulesetComparer(base_module, compare_module)
    data = comparer.get_diff_data()
    return data


def download_rule_set_from_git(country):
    pass


def create_report_scheduler(json_data):
    try:
        parser = CreateReportSchedulerTaskParser(json_data)
        info_model = ReportSchedulerInfo.objects.create_task(parser.base_env_id,
                                                             parser.compare_env_id,
                                                             parser.module_id,
                                                             parser.country_list,
                                                             parser.mail_list,
                                                             parser.interval_hour,
                                                             parser.utc_time)

        run_report_scheduler(info_model.id, parser.base_env_id, parser.compare_env_id,
                             parser.country_list, parser.mail_list, parser.local_time,
                             parser.interval_hour)
        return info_model
    except BaseException:
        traceback.print_exc()
        logging.error(traceback.format_exc())


def update_report_scheduler(json_data):
    try:
        parser = UpdateReportSchedulerTaskParser(json_data)
        delete_scheduler(parser.task_id)
        info_model = create_report_scheduler(json_data)
        return info_model
    except BaseException:
        traceback.print_exc()
        logging.error(traceback.format_exc())


def delete_scheduler(task_id):
    try:
        ReportSchedulerInfo.objects.filter(id=task_id).delete()
    except BaseException:
        traceback.print_exc()
        logging.error(traceback.format_exc())


def run_report_scheduler(model_id, base_env_id, compare_env_id, country_list,
                         mail_list, next_proceed_time, interval):
    daily_task = DailyCompareReportTask(model_id,
                                        base_env_id,
                                        compare_env_id,
                                        country_list,
                                        mail_list)
    print("run_report_scheduler, task id:"+str(daily_task.id))
    scheduler = SendMailScheduler(daily_task.scheduler_listener)
    job = scheduler.test_job(daily_task.run_task, interval, next_proceed_time)
    daily_task.set_scheduled_job(job)


def restart_all_scheduler():
    try:
        logging.info("restart all scheduler")
        scheduler_model_list = ReportSchedulerInfo.objects.all()
        for scheduler in scheduler_model_list:
            country_list = scheduler.country_list.values("id")
            parser = DBReportSchedulerParser(scheduler, country_list)
            ReportSchedulerInfo.objects.update_next_proceed_time(parser.task_id,
                                                                 parser.utc_time)
            run_report_scheduler(parser.task_id,
                                 parser.base_env_id,
                                 parser.compare_env_id,
                                 parser.country_list,
                                 parser.mail_list,
                                 parser.local_time,
                                 parser.interval_hour)

        logging.info("restart all scheduler success")
    except BaseException:
        traceback.print_exc()
        logging.error(traceback.format_exc())
