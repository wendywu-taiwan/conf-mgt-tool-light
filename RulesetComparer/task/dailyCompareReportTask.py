import traceback

from RulesetComparer.task.compareRuleListTask import CompareRuleListTask
from RulesetComparer.utils.logger import *
from RulesetComparer.utils import fileManager, timeUtil
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.properties import config
from django.template.loader import render_to_string
from RulesetComparer.models import Environment, ReportSchedulerInfo
from RulesetComparer.date_model.json_builder.compare_report_info import CompareReportInfoBuilder
from RulesetComparer.task.baseSchedulerTask import BaseSchedulerTask


class DailyCompareReportTask(BaseSchedulerTask):

    def __init__(self, parser):
        BaseSchedulerTask.__init__(self)
        self.logger = "DailyCompareReportTask(%s)" % parser.task_id
        self.task_id = parser.task_id
        self.base_env = Environment.objects.get(id=parser.base_env_id)
        self.compare_env = Environment.objects.get(id=parser.compare_env_id)
        self.country_list = parser.country_list
        self.mail_content_type_list = parser.mail_content_type_list
        self.mail_list = parser.mail_list
        self.file_name_list = list()
        self.mail_sender = None
        self.info_builder = None

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
                    # add attachment
                    file_path = fileManager.get_compare_result_full_file_name("_html", task.compare_hash_key)
                    file_name = current_time + "_" + self.base_env.name + "_" + self.compare_env.name + "_" + country.name + "_" + "compare_report.html"
                    application = "text"
                    self.mail_sender.add_attachment(file_path, file_name, application)

                self.mail_sender.set_receiver(self.mail_list)
                self.mail_sender.compose_msg(subject, None, html_content)
                self.mail_sender.send()
                self.mail_sender.quit()
            except Exception as e:
                error_log(e)
                error_log(traceback.format_exc())

    def task_enable(self):
        task = ReportSchedulerInfo.objects.get(id=self.task_id)
        if task.enable == 1:
            return True
        else:
            return False

    def task_exist(self):
        task_count = ReportSchedulerInfo.objects.filter(id=self.task_id).count()
        if task_count == 0:
            return False
        else:
            return True

    def has_new_job(self):
        try:
            task = ReportSchedulerInfo.objects.get(id=self.task_id)
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
            error_log(e)
            raise e

    def update_next_run_time(self):
        if ReportSchedulerInfo.objects.filter(id=self.task_id).count() == 0:
            return

        time_zone = config.TIME_ZONE.get('asia_taipei')
        time_format = config.TIME_FORMAT.get('db_time_format')
        next_date_time = self.scheduled_job.next_run_time
        next_proceed_time = timeUtil.date_time_change_format(next_date_time, time_format)
        utc_next_proceed_time = timeUtil.local_time_to_utc(next_proceed_time, time_zone)

        task = ReportSchedulerInfo.objects.get(id=self.task_id)
        task.last_proceed_time = task.next_proceed_time
        task.next_proceed_time = utc_next_proceed_time

        task.save()
        info_log(self.logger, "update_next_run_time : %s" % next_date_time)

    def on_task_success(self):
        pass

    def on_task_failure(self):
        pass
