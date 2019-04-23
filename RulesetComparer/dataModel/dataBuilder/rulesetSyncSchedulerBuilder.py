import traceback
import ast
from RulesetComparer.properties import config
from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, ModuleSerializer
from RulesetComparer.utils.logger import *


class RulesetSyncSchedulerBuilder(BaseBuilder):

    def __init__(self, scheduler):
        self.scheduler = scheduler
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        try:
            self.__build_scheduler_json__()
        except Exception:
            self.result_dict[KEY_EXCEPTION] = self.scheduler

    def __build_scheduler_json__(self):
        self.result_dict[KEY_TASK_ID] = self.scheduler.id
        self.result_dict[KEY_SOURCE_ENV] = EnvironmentSerializer(self.scheduler.source_environment).data
        self.result_dict[KEY_TARGET_ENV] = EnvironmentSerializer(self.scheduler.target_environment).data
        self.result_dict[KEY_COUNTRY_LIST] = CountrySerializer(self.scheduler.country_list, many=True).data
        self.result_dict[ACTION_LIST] = self.get_action_list()
        self.result_dict[KEY_RECEIVER_LIST] = self.get_mail_list()
        self.result_dict[KEY_INTERVAL_HOUR] = self.scheduler.interval_hour
        self.result_dict[KEY_LAST_PROCEED_TIME] = self.get_format_time(self.scheduler.last_proceed_time)
        self.result_dict[KEY_NEXT_PROCEED_TIME] = self.get_format_time(self.scheduler.next_proceed_time)
        self.result_dict[KEY_BACKUP] = bool(self.scheduler.backup)
        self.result_dict[KEY_ENABLE] = bool(self.scheduler.enable)

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
