from RulesetComparer.utils.fileManager import clear_folder_over_days
from RulesetComparer.properties import config
from django.template.loader import render_to_string
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.dataModel.dataBuilder.jobFailureContentBuilder import JobFailureContentBuilder
from RulesetComparer.dataModel.dataBuilder.jobSuccessContentBuilder import JobSuccessContentBuilder
from RulesetComparer.b2bRequestTask.baseSchedulerTask import BaseSchedulerTask
import traceback


class ClearRulesetFilesTask(BaseSchedulerTask):
    RULESET_FOLDER_EXCEPTION = ["Git", "zip", "backup", "__init__.py"]

    def __init__(self):
        BaseSchedulerTask.__init__(self)
        self.logger = "ClearRulesetFilesTask"
        self.delete_zip_files = None
        self.delete_rulesets = None
        self.run_task_error = None
        self.tracback = None

    def set_scheduled_job(self, scheduled_job):
        super().set_scheduled_job(scheduled_job)

    def run_task(self):
        super().run_task()

    def execute(self):
        zip_file_path = config.get_file_path("rule_set_zip_file_path")
        ruleset_file_path = config.get_file_path("rule_set_path")
        ruleset_except_array = self.RULESET_FOLDER_EXCEPTION
        try:
            # clear zip file over 3 days
            self.delete_zip_files = clear_folder_over_days(zip_file_path, 1, None)

            # clear ruleset file over 3 days
            self.delete_rulesets = clear_folder_over_days(ruleset_file_path, 1, ruleset_except_array)
        except BaseException as e:
            self.run_task_error = e
            self.tracback = traceback.format_exc()

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
        # send mail
        mail_sender = MailSender(config.SEND_COMPARE_RESULT_MAIL)
        if self.run_task_error is None:
            builder = JobSuccessContentBuilder(self.logger)
            builder.generate_clear_rulesets_files_data(self.delete_rulesets, self.delete_zip_files)
            html_content = render_to_string('job_success_notice_content.html', builder.get_data())

        else:
            builder = JobFailureContentBuilder(self.logger, self.run_task_error, self.tracback)
            html_content = render_to_string('job_error_notice_content.html', builder.get_data())

        mail_sender.set_receiver(config.SEND_COMPARE_RESULT_MAIL.get("receivers"))
        mail_sender.compose_msg(None, None, html_content)
        mail_sender.send()
        mail_sender.quit()

    def on_task_failure(self):
        pass
