import traceback
from shutil import copyfile

from RulesetComparer.models import ReportSchedulerInfo
from common.task.daily_report import DailyReportTask
from RulesetComparer.task.compare_ruleset_list import CompareRuleListTask
from RulesetComparer.utils.logger import *
from RulesetComparer.utils import fileManager, timeUtil
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.properties import config
from django.template.loader import render_to_string
from RulesetComparer.date_model.json_builder.compare_report_info import CompareReportInfoBuilder
from common.properties.config import RULESET_ZIP_PATH, RULESET_ZIP_FILE_PATH, \
    RULESET_COMPARE_RESULT_ZIP_RESOURCE, RULESET_COMPARE_RESULT_HTML, RULESET_COMPARE_RESULT_FOLDER_PATH
from RulesetComparer.utils.fileManager import create_folder, archive_file_with_arcname, clear_folder
from permission.models import Environment


class RulesetDailyReportTask(DailyReportTask):

    def __init__(self, parser):
        self.logger = "RulesetDailyReportTask(%s)" % parser.task_id
        self.base_env = Environment.objects.get(id=parser.base_env_id)
        self.compare_env = Environment.objects.get(id=parser.compare_env_id)
        self.country_list = parser.country_list
        self.mail_content_type_list = parser.mail_content_type_list
        DailyReportTask.__init__(self, parser, ReportSchedulerInfo)

    def set_scheduled_job(self, scheduled_job):
        super().set_scheduled_job(scheduled_job)

    def run_task(self):
        super().run_task()

    def task_runnable(self):
        return super().task_runnable()

    def execute(self):
        current_time = timeUtil.get_format_current_time(config.TIME_FORMAT.get("year_month_date"))

        for country in self.country_list:
            try:
                task = CompareRuleListTask(self.base_env.id, self.compare_env.id, country.id)
                self.mail_sender = MailSender(config.SEND_COMPARE_RESULT_MAIL)

                # generate subject
                subject = config.SEND_COMPARE_RESULT_MAIL.get(
                    "title") + " for " + country.name + " - " + self.base_env.name + " <> " + self.compare_env.name

                # generate mail content
                result_data = fileManager.load_compare_result_file(task.compare_hash_key)
                info_builder = CompareReportInfoBuilder(result_data, self.mail_content_type_list)
                content_json = info_builder.get_data()
                html_content = render_to_string('compare_info_mail_content.html', content_json)

                if content_json[COMPARE_RESULT_HAS_CHANGES]:
                    # copy report to single folder
                    copy_path = RULESET_COMPARE_RESULT_FOLDER_PATH % str(task.compare_hash_key)
                    create_folder(copy_path)

                    resource_full_path = RULESET_COMPARE_RESULT_HTML % task.compare_hash_key
                    copy_full_path = RULESET_COMPARE_RESULT_ZIP_RESOURCE % (
                        task.compare_hash_key, task.compare_hash_key)
                    copyfile(resource_full_path, copy_full_path)

                    # archive single folder report
                    zip_file_path = RULESET_ZIP_FILE_PATH % task.compare_hash_key
                    archive_file_with_arcname(copy_path, RULESET_ZIP_PATH, zip_file_path)
                    clear_folder(copy_path)

                    file_name = current_time + "_" + self.base_env.name + "_" + self.compare_env.name + "_" + country.name + "_" + "compare_report.zip"
                    application = "text"
                    self.mail_sender.add_attachment(zip_file_path, file_name, application)

                self.mail_sender.set_receiver(self.mail_list)
                self.mail_sender.compose_msg(subject, None, html_content)
                self.mail_sender.send()
                self.mail_sender.quit()
            except Exception as e:
                error_log(e)
                error_log(traceback.format_exc())

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
