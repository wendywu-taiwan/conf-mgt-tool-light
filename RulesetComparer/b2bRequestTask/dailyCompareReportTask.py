import traceback
from RulesetComparer.properties.dataKey import COMPARE_RESULT_HAS_CHANGES
from RulesetComparer.utils.logger import *
from RulesetComparer.services import services
from RulesetComparer.utils import fileManager, timeUtil
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.properties import config
from django.template.loader import render_to_string
from RulesetComparer.models import Environment, ReportSchedulerInfo
from RulesetComparer.dataModel.dataBuilder.compareReportInfoBuilder import CompareReportInfoBuilder


class DailyCompareReportTask:
    LOG_CLASS = "DailyCompareReportTask"

    def __init__(self, task_id, base_env_id, compare_env_id, country_list, mail_content_type_list, mail_list):
        self.id = task_id
        self.scheduled_job = None
        self.base_env = Environment.objects.get(id=base_env_id)
        self.compare_env = Environment.objects.get(id=compare_env_id)
        self.country_list = country_list
        self.mail_content_type_list = mail_content_type_list
        self.mail_list = mail_list
        self.file_name_list = list()
        self.mail_sender = None
        self.info_builder = None

    def set_scheduled_job(self, scheduled_job):
        self.scheduled_job = scheduled_job

    def run_task(self):
        error_log("DailyCompareReportTask,run task id :" + str(self.id))
        task_exist = ReportSchedulerInfo.objects.filter(id=self.id).count()

        if task_exist == 0:
            self.scheduled_job.remove()
            error_log("DailyCompareReportTask remove task, id:" + str(self.id))
        else:
            self.send_mail()

    def send_mail(self):
        try:
            current_time = timeUtil.get_format_current_time(config.TIME_FORMAT.get("year_month_date"))
            base_env = Environment.objects.get(id=self.base_env.id)
            compare_env = Environment.objects.get(id=self.compare_env.id)

            for country in self.country_list:
                task = services.compare_rule_list_rule_set(self.base_env.id,
                                                           self.compare_env.id,
                                                           country.id)

                self.mail_sender = MailSender(config.SEND_COMPARE_RESULT_MAIL)

                # generate subject
                subject = config.SEND_COMPARE_RESULT_MAIL.get(
                    "title") + " for " + country.name + " - " + base_env.name + " <> " + compare_env.name

                # generate mail content
                result_data = fileManager.load_compare_result_file(task.compare_hash_key)
                info_builder = CompareReportInfoBuilder(result_data, self.mail_content_type_list)
                content_json = info_builder.get_data()
                html_content = render_to_string('compare_info_mail_content.html', content_json)

                if content_json[COMPARE_RESULT_HAS_CHANGES]:
                    # add attachment
                    file_path = fileManager.get_compare_result_full_file_name("_html", task.compare_hash_key)
                    file_name = current_time + "_" + base_env.name + "_" + compare_env.name + "_" + country.name + "_" + "compare_report.html"
                    application = "text"
                    self.mail_sender.add_attachment(file_path, file_name, application)

                self.mail_sender.set_receiver(self.mail_list)
                self.mail_sender.compose_msg(subject, None, html_content)
                self.mail_sender.send()
                self.mail_sender.quit()
        except Exception as e:
            error_log(traceback.format_exc())
            raise e

    def scheduler_listener(self, event):
        if event.exception:
            # send mail to wendy
            error_log('DailyCompareReportTask job crashed, task id =' + str(self.id))
            error_log(traceback.format_exc())
        else:
            try:
                info_log(self.LOG_CLASS, 'job worked, task id =' + str(self.id))
                time_zone = config.TIME_ZONE.get('asia_taipei')
                time_format = config.TIME_FORMAT.get('db_time_format')
                next_date_time = self.scheduled_job.next_run_time
                next_proceed_time = timeUtil.date_time_change_format(next_date_time, time_format)
                utc_next_proceed_time = timeUtil.local_time_to_utc(next_proceed_time, time_zone)

                task = ReportSchedulerInfo.objects.get(id=self.id)
                task.last_proceed_time = task.next_proceed_time
                task.next_proceed_time = utc_next_proceed_time

                task.save()
            except BaseException:
                error_log(traceback.format_exc())
