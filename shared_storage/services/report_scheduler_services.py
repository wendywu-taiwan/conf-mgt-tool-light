from permission.data_object.permission_checker import SharedStorageReportPermissionChecker
from RulesetComparer.utils.logger import info_log
from shared_storage.models import SharedStorageReportScheduler
from shared_storage.data_object.json_parser.create_report_scheduler import CreateReportSchedulerParser
from shared_storage.data_object.json_parser.delete_report_scheduler import DeleteReportSchedulerParser
from shared_storage.data_object.json_parser.update_report_scheduler_status import UpdateReportSchedulerStatusParser
from shared_storage.data_object.json_parser.db_report_scheduler import DBReportSchedulerParser
from shared_storage.task.shared_storage_daily_report import SharedStorageDailyReportTask
from common.services.scheduler_services import create_scheduler_job

LOG_CLASS = "SharedStorageReportSchedulerService"


def restart_schedulers():
    try:
        schedulers = SharedStorageReportScheduler.objects.all()
        if len(schedulers) == 0:
            return

        info_log(LOG_CLASS, "restart all schedulers")
        for scheduler in schedulers:
            parser = DBReportSchedulerParser(scheduler)
            SharedStorageReportScheduler.objects.update_next_proceed_time(parser.task_id, parser.utc_time)
            add_task_to_scheduler(parser)
        info_log(LOG_CLASS, "restart all success")

    except Exception as e:
        raise e


def get_schedulers():
    schedulers = SharedStorageReportScheduler.objects.all()
    return schedulers


def create_scheduler(json_data, user):
    SharedStorageReportPermissionChecker(user)
    parser = CreateReportSchedulerParser(json_data)
    scheduler = SharedStorageReportScheduler.objects.create_task(parser.left_data_center_id,
                                                                 parser.right_data_center_id,
                                                                 parser.left_environment_id,
                                                                 parser.right_environment_id,
                                                                 parser.left_folder, parser.right_folder,
                                                                 parser.mail_list,
                                                                 parser.frequency_type, parser.interval,
                                                                 parser.utc_time)

    parser.task_id = scheduler.id
    add_task_to_scheduler(parser)
    return scheduler


def update_scheduler(json_data, user):
    SharedStorageReportPermissionChecker(user)
    parser = CreateReportSchedulerParser(json_data)
    report_scheduler = SharedStorageReportScheduler.objects.update_task(parser.task_id,
                                                                        parser.left_data_center_id,
                                                                        parser.right_data_center_id,
                                                                        parser.left_environment_id,
                                                                        parser.right_environment_id,
                                                                        parser.left_folder, parser.right_folder,
                                                                        parser.mail_list,
                                                                        parser.frequency_type,
                                                                        parser.interval,
                                                                        parser.utc_time)
    add_task_to_scheduler(parser)
    return report_scheduler


def delete_scheduler(json_data, user):
    SharedStorageReportPermissionChecker(user)
    parser = DeleteReportSchedulerParser(json_data)
    SharedStorageReportScheduler.objects.filter(id=parser.task_id).delete()


def update_scheduler_status(json_data, user):
    SharedStorageReportPermissionChecker(user)
    parser = UpdateReportSchedulerStatusParser(json_data)
    task = SharedStorageReportScheduler.objects.update_task_status(parser.task_id, parser.enable)
    return task


def add_task_to_scheduler(parser):
    task = SharedStorageDailyReportTask(parser)
    job = create_scheduler_job(task, parser)
    SharedStorageReportScheduler.objects.update_job_id(parser.task_id, job.id)
    task.set_scheduled_job(job)
