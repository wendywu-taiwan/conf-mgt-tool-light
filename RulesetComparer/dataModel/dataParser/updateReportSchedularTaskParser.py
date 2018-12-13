import traceback
from datetime import datetime
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
            self.mail_list = json_data.get("mail_list")
            self.interval_hour = json_data.get("interval_hour")
            # hh:mm:ss
            self.start_date_time = self.parse_start_date_time(json_data.get("start_date_time"))
            self.enable = dataKey.STATUS_ENABLE
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
            frontend_time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')

            date_time = timeUtil.time_to_date_time(start_date_time, frontend_time_format)
            local_time = timeUtil.date_time_change_time_zone(date_time, time_zone)
            current_date_time = timeUtil.get_current_date_time()

            local_time_hour = local_time.hour
            current_time_hour = current_date_time.hour

            # compare local time and current time
            if local_time > current_date_time:
                result_time = local_time
            else:
                local_time = local_time.replace(year=current_date_time.year)
                local_time = local_time.replace(month=current_date_time.month)
                if local_time_hour < current_time_hour:
                    local_time = local_time.replace(day=current_date_time.day + 1)
                else:
                    local_time = local_time.replace(day=current_date_time.day)
                result_time = local_time

            # use result time to create no time zone date time
            naive_result_time = datetime(result_time.year, result_time.month, result_time.day, result_time.hour,
                                         result_time.minute, result_time.second)
            # transfer time zone to utc
            utc_time = timeUtil.local_time_to_utc(naive_result_time, time_zone)
            return utc_time

        except Exception:
            traceback.print_exc()
