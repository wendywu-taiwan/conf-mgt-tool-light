from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from RulesetComparer.utils import timeUtil

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 1
}


class CustomJobScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone="Asia/Taipei")
        self.scheduler.start()

    def add_months_job(self, execute_func, month_interval, start_date):
        week_interval = month_interval * 4
        job = self.scheduler.add_job(func=execute_func, trigger='interval', weeks=week_interval,
                                     start_date=start_date)
        return job

    def add_weeks_job(self, execute_func, interval, start_date):
        job = self.scheduler.add_job(func=execute_func, trigger='interval', weeks=interval,
                                     start_date=start_date)
        return job

    def add_days_job(self, execute_func, interval, start_date):
        job = self.scheduler.add_job(func=execute_func, trigger='interval', days=interval,
                                     start_date=start_date)
        return job

    def add_hours_job(self, execute_func, interval, start_date):
        job = self.scheduler.add_job(func=execute_func, trigger='interval', hours=interval,
                                     start_date=start_date)
        return job

    def add_hours_job_now(self, execute_func, interval):
        start_time = timeUtil.add_minute(timeUtil.get_current_date_time(), 1)
        job = self.scheduler.add_job(func=execute_func, trigger='interval', hours=interval,
                                     start_date=start_time)
        return job

    def add_minutes_job(self, execute_func, interval, start_date):
        job = self.scheduler.add_job(func=execute_func, trigger='interval', minutes=interval,
                                     start_date=start_date)
        return job

    def print_jobs(self):
        self.scheduler.print_jobs()
