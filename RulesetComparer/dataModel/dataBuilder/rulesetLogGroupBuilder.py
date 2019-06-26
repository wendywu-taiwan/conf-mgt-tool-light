import traceback

from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.utils.logger import error_log
from RulesetComparer.utils.timeUtil import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.dataModel.dataBuilder.environmentBuilder import EnvironmentBuilder
from RulesetComparer.dataModel.dataBuilder.countryBuilder import CountryBuilder
from django.contrib.auth.models import User


class RulesetLogGroupBuilder(BaseBuilder):
    AUTHOR_TASK_MANAGER = "Task Manager"

    def __init__(self, data):
        try:
            self.data = data
            self.update_time = self.get_format_time(self.data.get(KEY_UPDATE_TIME))
            self.backup_key = self.data.get(KEY_BACKUP_KEY)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.data.get(KEY_ID)
        self.result_dict[KEY_BACKUP_KEY] = self.backup_key
        self.result_dict[KEY_UPDATE_TIME] = self.update_time
        self.result_dict[KEY_TASK_ID] = self.data.get(KEY_TASK_ID)
        self.result_dict[KEY_SOURCE_ENV] = self.parse_environment(self.data.get(KEY_SOURCE_ENV_ID))
        self.result_dict[KEY_TARGET_ENV] = self.parse_environment(self.data.get(KEY_TARGET_ENV_ID))
        self.result_dict[KEY_USER_NAME] = self.parse_user(self.data.get(KEY_AUTHOR_ID))
        self.result_dict[KEY_COUNTRY] = self.parse_country(self.data.get(KEY_COUNTRY_ID))
        self.result_dict[KEY_COMMIT_SHA] = self.data.get(KEY_COMMIT_SHA)
        self.result_dict[KEY_LOG_COUNT] = self.data.get(KEY_LOG_COUNT)

    def update_log_count(self, log_count):
        self.result_dict[KEY_LOG_COUNT] = log_count

    def parse_user(self, user_id):
        if user_id is None:
            return self.AUTHOR_TASK_MANAGER

        user = User.objects.get(id=user_id)
        return user.username

    @staticmethod
    def parse_country(country_id):
        country = Country.objects.get(id=country_id)
        return CountryBuilder(country).get_data()

    @staticmethod
    def parse_environment(environment_id):
        if environment_id is None:
            return EnvironmentBuilder(None).get_data()

        environment = Environment.objects.get(id=environment_id)
        return EnvironmentBuilder(environment).get_data()

    @staticmethod
    def get_format_time(utc_date_time):
        try:
            if utc_date_time is None:
                return None

            time_zone = TIME_ZONE.get('asia_taipei')
            time_format = TIME_FORMAT.get('db_time_format')

            naive_time = get_naive_time(utc_date_time.year, utc_date_time.month, utc_date_time.day,
                                        utc_date_time.hour, utc_date_time.minute, utc_date_time.second)

            local_date_time = utc_to_locale_time(naive_time, time_zone)
            str_time = date_time_to_time(local_date_time, time_format)
            return str_time
        except Exception as e:
            error_log(traceback.format_exc())
            raise e
