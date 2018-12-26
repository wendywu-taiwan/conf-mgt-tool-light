import traceback
from RulesetComparer.models import Country
from RulesetComparer.utils import timeUtil
from RulesetComparer.utils.logger import *
from RulesetComparer.properties import config, dataKey


class UpdateReportSchedulerTaskParser:

    def __init__(self, json_data):
        try:
            self.task_id = json_data.get("id")
            self.base_env_id = json_data.get("base_environment_id")
            self.compare_env_id = json_data.get("compare_environment_id")
            self.country_list = self.parse_country(json_data.get("country_list"))
            self.mail_list = json_data.get("mail_list")
            self.interval_hour = int(json_data.get("interval_hour"))
            self.local_time = self.parse_local_time(json_data.get("start_date_time"))
            self.utc_time = self.parse_utc_time(json_data.get("start_date_time"))
            self.enable = dataKey.STATUS_ENABLE
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

    def get_compare_time(self, start_date_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            frontend_time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')

            date_time = timeUtil.time_to_date_time(start_date_time, frontend_time_format)
            local_date_time = timeUtil.date_time_change_time_zone(date_time, time_zone)
            current_date_time = timeUtil.get_current_date_time()

            # compare local time and current time
            if local_date_time > current_date_time:
                result_time = local_date_time
            else:
                local_date_time = local_date_time.replace(year=current_date_time.year)
                local_date_time = local_date_time.replace(month=current_date_time.month)
                if self.local_date_time_valid(local_date_time, current_date_time):
                    local_date_time = local_date_time.replace(day=current_date_time.day)
                else:
                    local_date_time = local_date_time.replace(day=current_date_time.day + 1)
                result_time = local_date_time

            naive_result_time = datetime(result_time.year, result_time.month, result_time.day,
                                         result_time.hour, result_time.minute, result_time.second)
            return naive_result_time

        except Exception:
            traceback.print_exc()
            error_log(traceback.format_exc())

    def parse_local_time(self, start_date_time):
        try:
            return self.get_compare_time(start_date_time)
        except Exception:
            traceback.print_exc()
            error_log(traceback.format_exc())

    def parse_utc_time(self, start_date_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            naive_result_time = self.get_compare_time(start_date_time)

            # transfer time zone to utc
            utc_time = timeUtil.local_time_to_utc(naive_result_time, time_zone)
            return utc_time
        except Exception:
            traceback.print_exc()
            error_log(traceback.format_exc())

    @staticmethod
    def local_date_time_valid(local_date_time, current_date_time):
        try:
            if local_date_time.hour < current_date_time.hour:
                return False
            elif local_date_time.hour > current_date_time.hour:
                return True
            # if same hour, compare minutes
            else:
                if local_date_time.minute < current_date_time.minute:
                    return False
                elif local_date_time.minute > current_date_time.minute:
                    return True
                # if same minute, compare second
                else:
                    if local_date_time.second > current_date_time.second:
                        return True
                    else:
                        return False
        except Exception:
            traceback.print_exc()
            error_log(traceback.format_exc())
