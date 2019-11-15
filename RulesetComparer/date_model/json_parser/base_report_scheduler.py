import ast
from ConfigManageTool.settings import CURRENT_TIME_ZONE
from RulesetComparer.models import Country, MailContentType
from RulesetComparer.utils.logger import *
from RulesetComparer.properties import config
from datetime import timedelta

from RulesetComparer.utils.timeUtil import change_time_zone, get_naive_time_by_time
from common.properties.region_setting import TIME_ZONE_SERVER


class BaseReportSchedulerParser:
    def __init__(self, local_json_time):
        self.local_run_time = self.get_local_time_shift_days(local_json_time)
        self.job_run_time = self.get_job_run_time(self.local_run_time)

    @staticmethod
    def parse_country_id_list(country_id_list):
        country_list = list()
        for country_id in country_id_list:
            country = Country.objects.get(id=country_id)
            country_list.append(country)
        return country_list

    @staticmethod
    def parse_mail_content_type_list(mail_content_type_list):
        content_type_list = list()
        for mail_content_type_id in mail_content_type_list:
            mail_content_type_obj = MailContentType.objects.get(id=mail_content_type_id)
            content_type_list.append(mail_content_type_obj)
        return content_type_list

    @staticmethod
    def parse_country(country_id_list):
        country_list = list()
        for country_id_map in country_id_list:
            country = Country.objects.get(id=country_id_map['id'])
            country_list.append(country)
        return country_list

    @staticmethod
    def parse_db_mail_content_type(mail_content_type_list):
        content_type_list = list()
        for mail_content_type in mail_content_type_list:
            mail_content_type_obj = MailContentType.objects.get(id=mail_content_type['id'])
            content_type_list.append(mail_content_type_obj)
        return content_type_list

    @staticmethod
    def db_time_to_date_time(start_date_time):
        naive_local_time = datetime(start_date_time.year, start_date_time.month, start_date_time.day,
                                    start_date_time.hour, start_date_time.minute, start_date_time.second)

        return timeUtil.utc_to_locale_time(naive_local_time, CURRENT_TIME_ZONE)

    @staticmethod
    def frontend_time_to_date_time(start_date_time):
        frontend_time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')

        date_time = timeUtil.time_to_date_time(start_date_time, frontend_time_format)
        return timeUtil.date_time_change_time_zone(date_time, CURRENT_TIME_ZONE)

    @staticmethod
    def frontend_time_to_utc_time(frontend_time):
        frontend_time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')
        date_time = timeUtil.time_to_date_time(frontend_time, frontend_time_format)
        utc_time = timeUtil.local_time_to_utc(date_time, CURRENT_TIME_ZONE)
        return utc_time

    def get_local_time_shift_days(self, local_date_time):
        current_date_time = timeUtil.get_current_date_time()
        result_time = local_date_time
        # compare local time and current time
        if local_date_time < current_date_time:
            result_time = result_time.replace(day=current_date_time.day,
                                              month=current_date_time.month,
                                              year=current_date_time.year)
            if not self.local_date_time_bigger(local_date_time, current_date_time):
                result_time = result_time + timedelta(days=1)

        naive_result_time = get_naive_time_by_time(result_time)

        current_time_zone = settings.CURRENT_TIME_ZONE
        if current_time_zone != TIME_ZONE_SERVER:
            result_time = change_time_zone(naive_result_time, current_time_zone, TIME_ZONE_SERVER)

        naive_result_time = get_naive_time_by_time(result_time)

        return naive_result_time

    @staticmethod
    def get_utc_time(naive_local_time):
        utc_time = timeUtil.local_time_to_utc(naive_local_time, CURRENT_TIME_ZONE)
        return utc_time

    @staticmethod
    def get_job_run_time(naive_local_time):
        result_time = naive_local_time
        current_time_zone = settings.CURRENT_TIME_ZONE
        if current_time_zone != TIME_ZONE_SERVER:
            result_time = change_time_zone(naive_local_time, current_time_zone, TIME_ZONE_SERVER)

        naive_result_time = get_naive_time_by_time(result_time)
        return naive_result_time

    @staticmethod
    def local_date_time_bigger(local_date_time, current_date_time):
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

    @staticmethod
    def parse_boolean_to_int(boolean):
        if boolean:
            return 1
        else:
            return 0

    @staticmethod
    def parse_int_to_boolean(int_value):
        if int_value == 0:
            return False
        else:
            return True

    @staticmethod
    def get_mail_list(receiver_list):
        return ast.literal_eval(receiver_list)

    @staticmethod
    def parse_text_list(text_list):
        return ast.literal_eval(text_list)
