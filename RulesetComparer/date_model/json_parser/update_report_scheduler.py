from RulesetComparer.date_model.json_parser.base_report_scheduler import BaseReportSchedulerParser
from RulesetComparer.properties import key


class UpdateReportSchedulerTaskParser(BaseReportSchedulerParser):

    def __init__(self, json_data):
        try:
            BaseReportSchedulerParser.__init__(self, json_data.get("start_date_time"))
            self.task_id = json_data.get("id")
            self.base_env_id = json_data.get("base_environment_id")
            self.compare_env_id = json_data.get("compare_environment_id")
            self.country_list = self.parse_country_id_list(json_data.get("country_list"))
            self.mail_content_type_list = self.parse_mail_content_type_list(json_data.get("mail_content_type_list"))
            self.mail_list = json_data.get("mail_list")
            self.interval_hour = int(json_data.get("interval_hour"))
            # utc time for saving to database
            self.utc_time = self.get_utc_time(self.local_time)
            self.enable = key.STATUS_ENABLE
        except Exception as e:
            raise e

    def parse_country_id_list(self, country_id_list):
        return super().parse_country_id_list(country_id_list)

    def parse_mail_content_type_list(self, mail_content_type_list):
        return super().parse_mail_content_type_list(mail_content_type_list)

    def frontend_time_to_date_time(self, start_date_time):
        return super().frontend_time_to_date_time(start_date_time)

    def get_utc_time(self, naive_local_time):
        return super().get_utc_time(naive_local_time)

    def get_local_time_shift_days(self, start_date_time):
        local_date_time = self.frontend_time_to_date_time(start_date_time)
        return super().get_local_time_shift_days(local_date_time)

    def local_date_time_bigger(self, local_date_time, current_date_time):
        return super().local_date_time_bigger(local_date_time, current_date_time)
