import traceback
from abc import abstractmethod
from RulesetComparer.utils.logger import *


class BaseSchedulerTask:

    def __init__(self):
        self.task_id = None
        self.scheduled_job = None
        self.logger = None
        self.run_task_error = None
        self.tracback = None

    def set_scheduled_job(self, scheduled_job):
        self.scheduled_job = scheduled_job

    def run_task(self):
        info_log(self.logger, '======== task start ========')
        try:
            self.update_next_run_time()

            if not self.task_runnable():
                info_log(self.logger, '======== task finish , not runnable ========')
                return

            self.execute()

            if self.run_task_error is None and self.tracback is None:
                self.on_task_success()
                info_log(self.logger, '======== task finish , success ========')
            else:
                self.on_task_failure()
                info_log(self.logger, '======== task finish , success with error ========')
        except Exception as e:
            info_log(self.logger, '======== task finish , fail ========')
            error_log(traceback.format_exc())
            raise e

    # check if task has been removed
    def task_runnable(self):
        if not self.task_exist():
            info_log(self.logger, "task not exist in database, remove task")
            self.scheduled_job.remove()
            return False
        elif self.has_new_job():
            info_log(self.logger, "task has new job, remove task")
            self.scheduled_job.remove()
            return False
        elif not self.task_enable():
            info_log(self.logger, "task status is pending")
            return False
        else:
            info_log(self.logger, "task status is running")
            return True

    @abstractmethod
    # check task status is enable or disable
    def task_enable(self):
        pass

    @abstractmethod
    def task_exist(self):
        pass

    @abstractmethod
    def has_new_job(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def update_next_run_time(self):
        pass

    @abstractmethod
    def on_task_success(self):
        pass

    @abstractmethod
    def on_task_failure(self):
        pass
