import traceback

from RulesetComparer.services import rulesetSyncUpService
from RulesetComparer.utils.logger import *
from RulesetComparer.utils import timeUtil
from RulesetComparer.properties import config
from RulesetComparer.models import RulesetSyncUpScheduler


class RulesetsSyncUpTask:
    LOG_CLASS = "RulesetSyncUpTask"

    def __init__(self, parser):
        self.parser = parser
        self.scheduled_job = None

    def set_scheduled_job(self, scheduled_job):
        self.scheduled_job = scheduled_job

    def run_task(self):
        info_log(self.LOG_CLASS, '======== ruleset sync up task start , task id : %s ========' % self.parser.task_id)
        try:
            if not self.task_runnable():
                info_log(self.LOG_CLASS, "remove task")
                self.scheduled_job.remove()
            elif not self.task_enable():
                info_log(self.LOG_CLASS, "task disable")
            else:
                info_log(self.LOG_CLASS, "task enable")
                for country in self.parser.country_list:
                    try:
                        result_data = rulesetSyncUpService.sync_up_rulesets(self.parser, country)
                        rulesetSyncUpService.send_mail(result_data)
                    except Exception as e:
                        error_log(e)
                        error_log(traceback.format_exc())
        except Exception as e:
            raise e

    # check if task has been removed
    def task_runnable(self):
        if self.task_exist() and not self.new_job():
            return True
        else:
            return False

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

    def new_job(self):
        try:
            task = RulesetSyncUpScheduler.objects.get(id=self.parser.task_id)
            db_job_id = task.job_id
            current_job_id = self.scheduled_job.id
            info_log(self.LOG_CLASS, "db_job_id:" + str(db_job_id))
            info_log(self.LOG_CLASS, "current_job_id:" + str(current_job_id))
            if db_job_id == current_job_id:
                return False
            else:
                return True
        except Exception as e:
            error_log(traceback.format_exc())
            error_log(e.__traceback__)
            raise e

    def listener(self, event):
        if event.exception:
            # send mail to wendy
            error_log(self.LOG_CLASS + ' job crashed')
            error_log(event.exception)
        else:
            info_log(self.LOG_CLASS, 'job done')
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            time_format = config.TIME_FORMAT.get('db_time_format')
            next_date_time = self.scheduled_job.next_run_time
            next_proceed_time = timeUtil.date_time_change_format(next_date_time, time_format)
            utc_next_proceed_time = timeUtil.local_time_to_utc(next_proceed_time, time_zone)

            task = RulesetSyncUpScheduler.objects.get(id=self.parser.task_id)
            RulesetSyncUpScheduler.objects.update_time(self.parser.task_id,
                                                       task.next_proceed_time,
                                                       utc_next_proceed_time)
        except BaseException as e:
            error_log(e)
            error_log(traceback.format_exc())

        info_log(self.LOG_CLASS, '======== ruleset sync up task finish ========')
