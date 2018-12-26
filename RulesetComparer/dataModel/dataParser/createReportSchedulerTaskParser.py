import traceback
from RulesetComparer.models import Country
from RulesetComparer.utils import timeUtil
from RulesetComparer.utils.logger import *
from RulesetComparer.properties import config


class CreateReportSchedulerTaskParser:

    def __init__(self, json_data):
        try:
            self.base_env_id = json_data.get("base_environment_id")
            self.compare_env_id = json_data.get("compare_environment_id")
            self.module_id = json_data.get("module_id")
            self.country_list = self.parse_country(json_data.get("country_list"))
            self.mail_list = json_data.get("mail_list")
            self.interval_hour = int(json_data.get("interval_hour"))
            self.local_time = self.parse_local_time(json_data.get("start_date_time"))
            self.utc_time = self.parse_utc_time(json_data.get("start_date_time"))
        except BaseException:
            traceback.print_exc()
            error_log(traceback.format_exc())

    @staticmethod
    def parse_country(country_id_list):
        try:
            country_list = list()
            for country_id in country_id_list:
                country = Country.objects.get(id=country_id)
                country_list.append(country)
            return country_list
        except BaseException:
            traceback.print_exc()
            error_log(traceback.format_exc())

    @staticmethod
    def parse_utc_time(start_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')

            # parse str time to date time
            date_time = timeUtil.time_to_date_time(start_time, time_format)
            # parse local date time to utc time
            utc_time = timeUtil.local_time_to_utc(date_time, time_zone)
            return utc_time
        except Exception:
            traceback.print_exc()
            error_log(traceback.format_exc())

    @staticmethod
    def parse_local_time(start_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')

            # parse str time to date time
            date_time = timeUtil.time_to_date_time(start_time, time_format)
            # parse local date time to utc time
            local_date_time = timeUtil.date_time_change_time_zone(date_time, time_zone)
            naive_time = datetime(local_date_time.year, local_date_time.month, local_date_time.day,
                                  local_date_time.hour, local_date_time.minute, local_date_time.second)
            return naive_time
        except Exception:
            traceback.print_exc()
            error_log(traceback.format_exc())
