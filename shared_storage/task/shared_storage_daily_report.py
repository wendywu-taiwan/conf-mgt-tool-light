from common.task.daily_report import DailyReportTask
from RulesetComparer.utils.logger import *
from shared_storage.services import compare_services
from shared_storage.models import SharedStorageReportScheduler


class SharedStorageDailyReportTask(DailyReportTask):

    def __init__(self, parser):
        self.logger = "SharedStorageDailyReport(%s)" % parser.task_id
        self.parser = parser
        DailyReportTask.__init__(self, parser, SharedStorageReportScheduler)

    def set_scheduled_job(self, scheduled_job):
        info_log(self.logger, "set scheduled job:" + str(scheduled_job.id))
        super().set_scheduled_job(scheduled_job)

    def run_task(self):
        super().run_task()

    def task_runnable(self):
        return super().task_runnable()

    def execute(self):
        result_json = compare_services.compare_shared_storage_folder(self.parser.left_data_center_id,
                                                                     self.parser.left_environment_id,
                                                                     self.parser.left_folder,
                                                                     self.parser.right_data_center_id,
                                                                     self.parser.right_environment_id,
                                                                     self.parser.right_folder,
                                                                     True,
                                                                     self.parser.regional_tag,
                                                                     self.parser.request_host)
        compare_services.send_shared_storage_compare_result_mail(result_json, self.parser.mail_list)

    def task_enable(self):
        return super().task_enable()

    def task_exist(self):
        return super().task_exist()

    def has_new_job(self):
        return super().has_new_job()

    def update_next_run_time(self):
        super().update_next_run_time()

    def on_task_success(self):
        pass

    def on_task_failure(self):
        pass
