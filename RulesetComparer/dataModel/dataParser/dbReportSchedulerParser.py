import ast
from datetime import datetime

from RulesetComparer.dataModel.dataParser.baseReportSchedulerParser import BaseReportSchedulerParser
from RulesetComparer.properties import config
from RulesetComparer.utils import timeUtil


class DBReportSchedulerParser(BaseReportSchedulerParser):

    def __init__(self, scheduler, country_list, mail_content_type_list):
        try:
            BaseReportSchedulerParser.__init__(self)
            self.task_id = scheduler.id
            self.base_env_id = scheduler.base_environment.id
            self.compare_env_id = scheduler.compare_environment.id
            self.module_id = scheduler.module.id
            self.country_list = self.parse_country(country_list)
            self.mail_content_type_list = self.parse_db_mail_content_type(mail_content_type_list)
            self.mail_list = self.get_mail_list(scheduler.mail_list)
            self.interval_hour = scheduler.interval_hour
            self.local_time = self.get_local_time_shift_days(scheduler.next_proceed_time)
            self.utc_time = self.get_utc_time(self.local_time)
        except BaseException as e:
            raise e

    def parse_country(self, country_id_list):
        return super().parse_country(country_id_list)

    def parse_db_mail_content_type(self, mail_content_type_list):
        return super().parse_db_mail_content_type(mail_content_type_list)

    @staticmethod
    def db_time_to_date_time(start_date_time):
        time_zone = config.TIME_ZONE.get('asia_taipei')

        naive_local_time = datetime(start_date_time.year, start_date_time.month, start_date_time.day,
                                    start_date_time.hour, start_date_time.minute, start_date_time.second)

        return timeUtil.utc_to_locale_time(naive_local_time, time_zone)

    def get_utc_time(self, naive_local_time):
        return super().get_utc_time(naive_local_time)

    def local_date_time_bigger(self, local_date_time, current_date_time):
        return super().local_date_time_bigger(local_date_time, current_date_time)

    def get_local_time_shift_days(self, start_date_time):
        local_date_time = self.db_time_to_date_time(start_date_time)
        return super().get_local_time_shift_days(local_date_time)

    @staticmethod
    def get_mail_list(mail_list):
        return ast.literal_eval(mail_list)
