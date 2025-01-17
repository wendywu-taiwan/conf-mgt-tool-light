import traceback
from ConfigManageTool.settings import CURRENT_TIME_ZONE
from RulesetComparer.properties.config import *
from RulesetComparer.utils.logger import error_log
from RulesetComparer.utils.timeUtil import *
from permission.models import Country
from common.data_object.json_builder.base import BaseBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.country import CountryBuilder
from django.contrib.auth.models import User


class RulesetLogGroupBuilder(BaseBuilder):
    AUTHOR_TASK_MANAGER = "Task Manager"

    def __init__(self, data):
        try:
            self.data = data
            self.id = self.data.get(KEY_ID)
            self.source_environment = self.parse_environment(self.data.get(KEY_SOURCE_ENV_ID))
            self.target_environment = self.parse_environment(self.data.get(KEY_TARGET_ENV_ID))
            self.update_time = self.get_format_time(self.data.get(KEY_UPDATE_TIME))
            self.country = self.parse_country(self.data.get(KEY_COUNTRY_ID))
            self.backup_key = self.data.get(KEY_BACKUP_KEY)
            self.user = self.parse_user(self.data.get(KEY_AUTHOR_ID))
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.id
        self.result_dict[KEY_BACKUP_KEY] = self.backup_key
        self.result_dict[KEY_UPDATE_TIME] = self.update_time
        self.result_dict[KEY_TASK_ID] = self.data.get(KEY_TASK_ID)
        self.result_dict[KEY_SOURCE_ENV] = self.source_environment
        self.result_dict[KEY_TARGET_ENV] = self.target_environment
        self.result_dict[KEY_USER_NAME] = self.user
        self.result_dict[KEY_COUNTRY] = self.country
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
        return EnvironmentBuilder(id=environment_id).get_data()

    @staticmethod
    def get_format_time(utc_date_time):
        try:
            if utc_date_time is None:
                return None

            time_zone = CURRENT_TIME_ZONE
            time_format = TIME_FORMAT.get('db_time_format')

            naive_time = get_naive_time(utc_date_time.year, utc_date_time.month, utc_date_time.day,
                                        utc_date_time.hour, utc_date_time.minute, utc_date_time.second)

            local_date_time = utc_to_locale_time(naive_time, time_zone)
            str_time = date_time_to_time(local_date_time, time_format)
            return str_time
        except Exception as e:
            error_log(traceback.format_exc())
            raise e
