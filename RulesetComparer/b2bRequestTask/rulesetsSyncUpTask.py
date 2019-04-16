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
        info_log(self.LOG_CLASS, '======== ruleset sync up task start ========')
        try:
            if self.task_runnable():
                for country in self.parser.country_list:
                    result_data = rulesetSyncUpService.sync_up_rulesets(self.parser, country)
                    rulesetSyncUpService.send_mail(result_data)
            else:
                error_log(self.LOG_CLASS + " remove task, id:" + str(self.parser.task_id))
                self.scheduled_job.remove()
        except Exception as e:
            raise e

    def task_runnable(self):
        task_count = RulesetSyncUpScheduler.objects.filter(id=self.parser.task_id).count()
        if task_count > 0:
            return True
        else:
            return False

    def listener(self, event):
        if event.exception:
            # send mail to wendy
            error_log(self.LOG_CLASS + ' job crashed')
            error_log(traceback.format_exc())
        else:
            try:
                time_zone = config.TIME_ZONE.get('asia_taipei')
                time_format = config.TIME_FORMAT.get('db_time_format')
                next_date_time = self.scheduled_job.next_run_time
                next_proceed_time = timeUtil.date_time_change_format(next_date_time, time_format)
                utc_next_proceed_time = timeUtil.local_time_to_utc(next_proceed_time, time_zone)

                task = RulesetSyncUpScheduler.objects.get(id=self.parser.task_id)
                task.last_proceed_time = task.next_proceed_time
                task.next_proceed_time = utc_next_proceed_time
                task.save()
                info_log(self.LOG_CLASS, 'job worked, id: ' + str(self.parser.task_id))
            except BaseException:
                error_log(traceback.format_exc())

            info_log(self.LOG_CLASS, '======== ruleset sync up task finish ========')
