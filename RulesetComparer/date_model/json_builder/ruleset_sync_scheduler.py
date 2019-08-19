import traceback
import ast
from RulesetComparer.properties import config
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleBaseBuilder
from RulesetComparer.utils.logger import *
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.country import CountryBuilder
from common.data_object.json_builder.user import UserBuilder


class RulesetSyncSchedulerBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user, scheduler):
        self.scheduler = scheduler
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        try:
            self.__build_scheduler_json__()
        except Exception as e:
            self.result_dict[KEY_EXCEPTION] = e

    def __build_scheduler_json__(self):
        self.result_dict[KEY_TASK_ID] = self.scheduler.id
        self.result_dict[KEY_SOURCE_ENV] = EnvironmentBuilder(environment=self.scheduler.source_environment).get_data()
        self.result_dict[KEY_TARGET_ENV] = EnvironmentBuilder(environment=self.scheduler.target_environment).get_data()
        self.result_dict[KEY_COUNTRY_LIST] = self.get_country_list()
        self.result_dict[ACTION_LIST] = self.get_action_list()
        self.result_dict[KEY_RECEIVER_LIST] = self.get_mail_list()
        self.result_dict[KEY_CREATOR] = UserBuilder(self.scheduler.creator).get_data()
        self.result_dict[KEY_EDITOR] = UserBuilder(self.scheduler.editor).get_data()
        self.result_dict[KEY_INTERVAL_HOUR] = self.scheduler.interval_hour
        self.result_dict[KEY_CREATED_TIME] = self.get_format_time(self.scheduler.created_time)
        self.result_dict[KEY_UPDATED_TIME] = self.get_format_time(self.scheduler.updated_time)
        self.result_dict[KEY_LAST_PROCEED_TIME] = self.get_format_time(self.scheduler.last_proceed_time)
        self.result_dict[KEY_NEXT_PROCEED_TIME] = self.get_format_time(self.scheduler.next_proceed_time)
        self.result_dict[KEY_ENABLE] = bool(self.scheduler.enable)

    def get_country_list(self):
        country_list = []
        for country in self.scheduler.country_list.all():
            country_data = CountryBuilder(country).get_data()
            country_list.append(country_data)
        return country_list

    def get_mail_list(self):
        try:
            return ast.literal_eval(self.scheduler.mail_list)
        except Exception:
            return self.scheduler.mail_list

    def get_action_list(self):
        try:
            return ast.literal_eval(self.scheduler.action_list)
        except Exception:
            return self.scheduler.action_list

    @staticmethod
    def get_format_time(utc_date_time):
        try:
            if utc_date_time is None:
                return None

            time_zone = config.TIME_ZONE.get('asia_taipei')
            time_format = config.TIME_FORMAT.get('db_time_format')

            naive_time = timeUtil.get_naive_time(utc_date_time.year, utc_date_time.month, utc_date_time.day,
                                                 utc_date_time.hour, utc_date_time.minute, utc_date_time.second)

            local_date_time = timeUtil.utc_to_locale_time(naive_time, time_zone)
            str_time = timeUtil.date_time_to_time(local_date_time, time_format)
            return str_time
        except Exception as e:
            error_log(traceback.format_exc())
            raise e


class RulesetSyncSchedulersBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user, schedulers):
        self.schedulers = schedulers
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        array = []
        for scheduler in self.schedulers:
            data = RulesetSyncSchedulerBuilder(None, scheduler).get_data()
            array.append(data)
        self.result_dict[KEY_DATA] = array
