from RulesetComparer.task.daily_compare_report import DailyCompareReportTask
from RulesetComparer.date_model.json_parser.create_report_scheduler import CreateReportSchedulerTaskParser
from RulesetComparer.date_model.json_parser.db_report_scheduler import DBReportSchedulerParser
from RulesetComparer.date_model.json_parser.delete_report_scheduler import DeleteReportSchedulerParser
from RulesetComparer.date_model.json_parser.update_report_scheduler_status import UpdateReportSchedulerStatusParser
from RulesetComparer.models import ReportSchedulerInfo
from RulesetComparer.utils.customJobScheduler import CustomJobScheduler
from RulesetComparer.utils.logger import info_log
from RulesetComparer.properties.key import *


def restart_schedulers():
    try:
        schedulers = ReportSchedulerInfo.objects.all()
        if len(schedulers) == 0:
            return

        info_log("rulesetReportSchedulerService", "restart all schedulers")
        for scheduler in schedulers:
            country_list = scheduler.country_list.values(KEY_ID)
            mail_content_type_list = scheduler.mail_content_type_list.values(KEY_ID)
            parser = DBReportSchedulerParser(scheduler, country_list, mail_content_type_list)
            ReportSchedulerInfo.objects.update_next_proceed_time(parser.task_id, parser.utc_time)
            add_task_to_scheduler(parser)
    except Exception as e:
        raise e


def get_schedulers():
    try:
        schedulers = ReportSchedulerInfo.objects.all()
        return schedulers
    except Exception as e:
        raise e


def create_scheduler(json_data, user):
    try:
        parser = CreateReportSchedulerTaskParser(json_data, user)
        report_scheduler = ReportSchedulerInfo.objects.create_task(parser.base_env_id,
                                                                   parser.compare_env_id,
                                                                   parser.module_id,
                                                                   parser.country_list,
                                                                   parser.mail_content_type_list,
                                                                   parser.mail_list,
                                                                   parser.interval_hour,
                                                                   parser.utc_time)

        parser.task_id = report_scheduler.id
        add_task_to_scheduler(parser)
        return report_scheduler
    except Exception as e:
        raise e


def update_report_scheduler(json_data, user):
    try:
        parser = CreateReportSchedulerTaskParser(json_data, user)
        report_scheduler = ReportSchedulerInfo.objects.update_task(parser.task_id,
                                                                   parser.base_env_id,
                                                                   parser.compare_env_id,
                                                                   parser.country_list,
                                                                   parser.mail_content_type_list,
                                                                   parser.mail_list,
                                                                   parser.interval_hour,
                                                                   parser.utc_time)
        add_task_to_scheduler(parser)
        return report_scheduler
    except Exception as e:
        raise e


def delete_scheduler(json_data, user):
    try:
        parser = DeleteReportSchedulerParser(json_data, user)
        ReportSchedulerInfo.objects.filter(id=parser.task_id).delete()
    except Exception as e:
        raise e


def add_task_to_scheduler(parser):
    daily_task = DailyCompareReportTask(parser)
    scheduler = CustomJobScheduler()
    job = scheduler.add_hours_job(daily_task.run_task, parser.interval_hour, parser.local_time)
    ReportSchedulerInfo.objects.update_job_id(parser.task_id, job.id)
    daily_task.set_scheduled_job(job)


def update_scheduler_status(json_data, user):
    parser = UpdateReportSchedulerStatusParser(json_data, user)
    task = ReportSchedulerInfo.objects.update_task_status(parser.task_id, parser.enable)
    return task