import ast
import traceback
from RulesetComparer.models import Country
from RulesetComparer.utils import timeUtil
from RulesetComparer.utils.logger import *
from RulesetComparer.properties import config


class DBReportSchedulerParser:

    def __init__(self, scheduler, country_list):
        try:
            self.task_id = scheduler.id
            self.base_env_id = scheduler.base_environment.id
            self.compare_env_id = scheduler.compare_environment.id
            self.module_id = scheduler.module.id
            self.country_list = self.parse_country(country_list)
            self.mail_list = self.get_mail_list(scheduler.mail_list)
            self.interval_hour = scheduler.interval_hour
            self.local_time = self.get_local_time(scheduler.next_proceed_time)
            self.utc_time = self.get_utc_time(self.local_time)
        except BaseException:
            traceback.print_exc()
            error_log(traceback.format_exc())

    @staticmethod
    def parse_country(country_id_list):
        try:
            country_list = list()
            for country_id_map in country_id_list:
                country = Country.objects.get(id=country_id_map['id'])
                country_list.append(country)
            return country_list
        except BaseException:
            traceback.print_exc()
            error_log(traceback.format_exc())

    @staticmethod
    def get_mail_list(mail_list):
        try:
            return ast.literal_eval(mail_list)
        except Exception:
            return mail_list

    def get_local_time(self, start_date_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')

            naive_utc_time = datetime(start_date_time.year, start_date_time.month, start_date_time.day,
                                      start_date_time.hour, start_date_time.minute, start_date_time.second)

            local_date_time = timeUtil.utc_to_locale_time(naive_utc_time, time_zone)
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

    @staticmethod
    def get_utc_time(naive_local_time):
        try:
            time_zone = config.TIME_ZONE.get('asia_taipei')
            utc_time = timeUtil.local_time_to_utc(naive_local_time, time_zone)
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
