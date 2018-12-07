import traceback
from RulesetComparer.models import Country
from RulesetComparer.utils import timeUtil
from RulesetComparer.properties import config, dataKey


class UpdateReportSchedulerTaskParser:

    def __init__(self, json_data):
        try:
            self.task_id = json_data.get("id")
            self.base_env_id = json_data.get("base_environment_id")
            self.compare_env_id = json_data.get("compare_environment_id")
            self.country_list = self.parse_country(json_data.get("country_list"))
            self.mail_list = self.parse_mail_list(json_data.get("mail_list"))
            self.interval_hour = json_data.get("interval_hour")
            # hh:mm:ss
            self.start_date_time = self.parse_start_date_time(json_data.get("proceed_time"))
            self.enable = self.parse_enable(json_data.get("enable"))
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
    def parse_mail_list(mail_list):
        string_compose = ","
        return string_compose.join(mail_list)

    @staticmethod
    def parse_start_date_time(start_date_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            frontend_time_format = config.TIME_FORMAT.get('hour_minute_second')
            db_time_format = config.TIME_FORMAT.get('db_time_format')

            frontend_date_time = timeUtil.time_to_date_time(start_date_time, frontend_time_format)
            add_year_month_day_date_time = timeUtil.get_date_time(hour=frontend_date_time.hour,
                                                                  minute=frontend_date_time.minute,
                                                                  second=frontend_date_time.second,
                                                                  time_zone=time_zone)

            current_date_time = timeUtil.get_current_date_time()
            if add_year_month_day_date_time > current_date_time:
                result_time = add_year_month_day_date_time
            else:
                result_time = timeUtil.date_time_add_day(add_year_month_day_date_time)

            result_time = timeUtil.date_time_to_date_time(result_time,db_time_format)
            return result_time

        except Exception:
            traceback.print_exc()

    @staticmethod
    def parse_enable(status):
        try:
            if status is True:
                return dataKey.STATUS_ENABLE
            else:
                return dataKey.STATUS_DISABLE
        except Exception:
            traceback.print_exc()
