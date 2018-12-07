from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 1
}


class SendMailScheduler:
    def __init__(self, listener):
        self.scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone="Asia/Taipei")
        self.scheduler.start()
        self.scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def add_job(self, send_mail_task, interval, start_date):
        job = self.scheduler.add_job(func=send_mail_task, trigger='interval', hour=interval,
                                     start_date=start_date)
        return job

    def test_job(self, send_mail_task, interval, start_date):
        job = self.scheduler.add_job(func=send_mail_task, trigger='interval', minutes=interval,
                                     start_date=start_date)
        return job

    def print_jobs(self):
        self.scheduler.print_jobs()
