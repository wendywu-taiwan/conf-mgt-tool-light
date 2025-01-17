import traceback
from ConfigManageTool.settings import CURRENT_TIME_ZONE
from RulesetComparer.date_model.data_object.log_group import RulesetLogGroupObj
from RulesetComparer.services import sync
from RulesetComparer.utils.logger import *
from RulesetComparer.utils import timeUtil
from RulesetComparer.properties import config
from RulesetComparer.models import RulesetSyncUpScheduler
from RulesetComparer.task.base_scheduler import BaseSchedulerTask
from django.contrib.auth.models import User


class RulesetsSyncUpTask(BaseSchedulerTask):

    def __init__(self, parser):
        BaseSchedulerTask.__init__(self)
        self.parser = parser
        self.logger = "RulesetSyncUpTask(%s)" % parser.task_id
        self.task_id = parser.task_id

    def set_scheduled_job(self, scheduled_job):
        info_log(self.logger, "set scheduled job:" + str(scheduled_job.id))
        super().set_scheduled_job(scheduled_job)

    def run_task(self):
        super().run_task()

    def execute(self):
        for country in self.parser.country_list:
            try:
                task = RulesetSyncUpScheduler.objects.get(id=self.task_id)
                user = User.objects.get(username=USER_NAME_TASK_MANAGER)
                rs_log_groups = RulesetLogGroupObj(self.parser, user, country)
                rs_log_groups.set_task(task)
                rs_log_groups.set_update_time(task.last_proceed_time)
                rs_log_groups.log_group()

                result_data = sync.sync_up_rulesets(rs_log_groups, self.parser, country)
                sync.send_mail(result_data, self.parser.receiver_list)
            except Exception as e:
                error_log(e)
                error_log(traceback.format_exc())
                error_log("Exception : country %s sync up ruleset fail" % country.name)

    def task_runnable(self):
        return super().task_runnable()

    # check task status is enable or disable
    def task_enable(self):
        task = RulesetSyncUpScheduler.objects.get(id=self.parser.task_id)
        if task.enable == 1:
            return True
        else:
            return False

    def task_exist(self):
        task_count = RulesetSyncUpScheduler.objects.filter(id=self.parser.task_id).count()
        if task_count == 0:
            return False
        else:
            return True

    def has_new_job(self):
        try:
            task = RulesetSyncUpScheduler.objects.get(id=self.parser.task_id)
            db_job_id = task.job_id
            current_job_id = self.scheduled_job.id
            info_log(self.logger, "db_job_id:" + str(db_job_id))
            info_log(self.logger, "current_job_id:" + str(current_job_id))
            if db_job_id == current_job_id:
                return False
            else:
                return True
        except Exception as e:
            error_log(traceback.format_exc())

    def update_next_run_time(self):
        if RulesetSyncUpScheduler.objects.filter(id=self.task_id).count() == 0:
            return

        time_format = config.TIME_FORMAT.get('db_time_format')
        next_date_time = self.scheduled_job.next_run_time
        next_proceed_time = timeUtil.date_time_change_format(next_date_time, time_format)
        utc_next_proceed_time = timeUtil.local_time_to_utc(next_proceed_time, CURRENT_TIME_ZONE)

        task = RulesetSyncUpScheduler.objects.get(id=self.task_id)
        RulesetSyncUpScheduler.objects.update_time(self.task_id,
                                                   task.next_proceed_time,
                                                   utc_next_proceed_time)
        info_log(self.logger, "update_next_run_time : %s" % next_date_time)

    def on_task_success(self):
        pass

    def on_task_failure(self):
        pass
