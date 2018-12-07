import traceback
from RulesetComparer.models import Country
from RulesetComparer.utils import timeUtil
from RulesetComparer.properties import config


class CreateReportSchedulerTaskParser:

    def __init__(self, json_data):
        try:
            self.base_env_id = json_data.get("base_environment_id")
            self.compare_env_id = json_data.get("compare_environment_id")
            self.module_id = json_data.get("module_id")
            self.country_list = self.parse_country(json_data.get("country_list"))
            self.mail_list = json_data.get("mail_list")
            self.interval_hour = json_data.get("interval_hour")
            self.start_date_time = self.parse_start_date_time(json_data.get("start_date_time"))
        except BaseException as e:
            traceback.print_exc()

    @staticmethod
    def parse_country(country_id_list):
        try:
            country_list = list()
            for country_id in country_id_list:
                country = Country.objects.get(id=country_id)
                country_list.append(country)
            return country_list
        except BaseException as e:
            traceback.print_exc()

    @staticmethod
    def parse_start_date_time(start_date_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')

            date_time = timeUtil.time_to_date_time(start_date_time, time_format)
            date_time = timeUtil.date_time_change_time_zone(date_time, time_zone)
            return date_time
        except Exception:
            traceback.print_exc()
