from RulesetComparer.utils.fileManager import clear_folder_over_days
from RulesetComparer.properties import config
from django.template.loader import render_to_string

from RulesetComparer.utils.logger import error_log
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.date_model.json_builder.job_failure_content import JobFailureContentBuilder
from RulesetComparer.date_model.json_builder.job_success_content import JobSuccessContentBuilder
from RulesetComparer.task.baseSchedulerTask import BaseSchedulerTask
import traceback


class BaseClearFilesTask(BaseSchedulerTask):

    def __init__(self):
        BaseSchedulerTask.__init__(self)
        self.logger = None
        self.expired_day = 1
        self.delete_files_path = None
        self.delete_files = None
        self.run_task_error = None
        self.tracback = None
        self.mail_setting = None
        self.not_removed_files_extension = []

    def set_scheduled_job(self, scheduled_job):
        super().set_scheduled_job(scheduled_job)

    def run_task(self):
        super().run_task()

    def execute(self):
        try:
            self.delete_files = clear_folder_over_days(self.delete_files_path, self.expired_day,
                                                       self.not_removed_files_extension)
        except BaseException as e:
            self.run_task_error = e
            self.tracback = traceback.format_exc()
            error_log(traceback.format_exc())
            raise e

    def task_runnable(self):
        return super().task_runnable()

    def task_enable(self):
        return True

    def task_exist(self):
        return True

    def has_new_job(self):
        return False

    def update_next_run_time(self):
        pass

    def on_task_success(self):
        try:
            builder = JobSuccessContentBuilder(self.logger)
            builder.generate_normal_files_data(self.delete_files)
            html_content = render_to_string('job_success_notice_content.html', builder.get_data())
            self.send_mail(html_content)
        except BaseException as e:
            self.run_task_error = e
            self.tracback = traceback.format_exc()
            raise e

    def on_task_failure(self):
        try:
            builder = JobFailureContentBuilder(self.logger, self.run_task_error, self.tracback)
            html_content = render_to_string('job_error_notice_content.html', builder.get_data())
            self.send_mail(html_content)
        except BaseException as e:
            self.run_task_error = e
            self.tracback = traceback.format_exc()
            raise e

    def send_mail(self, html_content):
        mail_sender = MailSender(self.mail_setting)
        mail_sender.set_receiver(self.mail_setting.get("receivers"))
        mail_sender.compose_msg(None, None, html_content)
        mail_sender.send()
        mail_sender.quit()
