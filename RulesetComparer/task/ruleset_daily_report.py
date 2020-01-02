import RulesetComparer.services

from RulesetComparer.models import ReportSchedulerInfo
from common.task.daily_report import DailyReportTask
from RulesetComparer.task.compare_ruleset_list import CompareRuleListTask
from RulesetComparer.utils.logger import *
from RulesetComparer.utils import fileManager
from django.template.loader import render_to_string
from RulesetComparer.date_model.json_builder.compare_report_info import CompareReportInfoBuilder
from permission.models import Environment


class RulesetDailyReportTask(DailyReportTask):

    def __init__(self, parser):
        self.logger = "RulesetDailyReportTask(%s)" % parser.task_id
        self.base_env = Environment.objects.get(id=parser.base_env_id)
        self.compare_env = Environment.objects.get(id=parser.compare_env_id)
        self.country_list = parser.country_list
        self.mail_content_type_list = parser.mail_content_type_list
        self.skip_ruleset_map = parser.skip_ruleset_map
        self.skip_rulesets = list()

        DailyReportTask.__init__(self, parser, ReportSchedulerInfo)

    def set_scheduled_job(self, scheduled_job):
        super().set_scheduled_job(scheduled_job)

    def run_task(self):
        super().run_task()

    def task_runnable(self):
        return super().task_runnable()

    def execute(self):
        for country in self.country_list:
            country_id = str(country.id)
            if country_id in self.skip_ruleset_map:
                self.skip_rulesets = self.skip_ruleset_map[country_id]
            task = CompareRuleListTask(self.base_env.id, self.compare_env.id, country.id, self.skip_rulesets)

            # generate mail content
            result_data = fileManager.load_compare_result_file(task.compare_hash_key)
            info_builder = CompareReportInfoBuilder(result_data, self.mail_content_type_list, self.skip_rulesets)
            content_json = info_builder.get_data()
            html_content = render_to_string('compare_info_mail_content.html', content_json)

            if content_json[COMPARE_RESULT_HAS_CHANGES]:
                zip_file_path = RulesetComparer.services.report_scheduler.generate_report_mail_attachment(task)
                RulesetComparer.services.report_scheduler.send_report_mail_with_attachment(country.name,
                                                                                           self.base_env.name,
                                                                                           self.compare_env.name,
                                                                                           html_content,
                                                                                           self.mail_list,
                                                                                           zip_file_path)
            else:
                RulesetComparer.services.report_scheduler.send_report_mail(country.name, self.base_env.name,
                                                                           self.compare_env.name, html_content,
                                                                           self.mail_list)

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
