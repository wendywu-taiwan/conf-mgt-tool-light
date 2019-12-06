import traceback
from RulesetComparer.utils.logger import *
from RulesetComparer.utils import timeUtil
from RulesetComparer.properties import config
from RulesetComparer.task.base_scheduler import BaseSchedulerTask


class DailyReportTask(BaseSchedulerTask):

    def __init__(self, parser, model):
        BaseSchedulerTask.__init__(self)
        self.model = model
        self.task_id = parser.task_id
        self.mail_list = parser.mail_list
        self.logger = None
        self.mail_sender = None
        self.info_builder = None

    def set_scheduled_job(self, scheduled_job):
        info_log(self.logger, "set scheduled job:" + str(scheduled_job.id))
        super().set_scheduled_job(scheduled_job)

    def run_task(self):
        super().run_task()

    def task_runnable(self):
        return super().task_runnable()

    def execute(self):
        pass

    def task_enable(self):
        task = self.model.objects.get(id=self.task_id)
        if task.enable == 1:
            return True
        else:
            return False

    def task_exist(self):
        task_count = self.model.objects.filter(id=self.task_id).count()
        if task_count == 0:
            return False
        else:
            return True

    def has_new_job(self):
        try:
            task = self.model.objects.get(id=self.task_id)
            db_job_id = task.job_id
            current_job_id = self.scheduled_job.id
            info_log(self.logger, "db_job_id: " + str(db_job_id))
            info_log(self.logger, "current_job_id: " + str(current_job_id))
            if db_job_id == current_job_id:
                return False
            else:
                return True
        except Exception as e:
            error_log(traceback.format_exc())
            error_log(e)
            raise e

    def update_next_run_time(self):
        if self.model.objects.filter(id=self.task_id).count() == 0:
            return

        time_format = config.TIME_FORMAT.get('db_time_format')
        next_date_time = self.scheduled_job.next_run_time
        next_proceed_time = timeUtil.date_time_change_format(next_date_time, time_format)
        utc_next_proceed_time = timeUtil.local_time_to_utc(next_proceed_time, CURRENT_TIME_ZONE)

        task = self.model.objects.get(id=self.task_id)
        task.last_proceed_time = task.next_proceed_time
        task.next_proceed_time = utc_next_proceed_time

        task.save()
        info_log(self.logger, "update_next_run_time : %s" % next_date_time)

    def on_task_success(self):
        pass

    def on_task_failure(self):
        pass
