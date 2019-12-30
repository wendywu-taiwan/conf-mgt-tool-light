import traceback
import ast
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from common.data_object.json_builder.base import BaseBuilder
from common.data_object.json_builder.frequency_type import FrequencyTypeBuilder
from common.utils.utility import parse_db_string_list


class ReportSchedulerBuilder(BaseBuilder):

    def __init__(self, scheduler):
        self.scheduler = scheduler
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_TASK_ID] = self.scheduler.id
        self.result_dict[KEY_MAIL_LIST] = parse_db_string_list(self.scheduler.mail_list)
        self.result_dict[KEY_FREQUENCY_TYPE] = FrequencyTypeBuilder(self.scheduler.frequency_type).get_data()
        self.result_dict[KEY_INTERVAL] = self.scheduler.interval
        self.result_dict[KEY_LAST_PROCEED_TIME] = self.get_format_time(self.scheduler.last_proceed_time)
        self.result_dict[KEY_NEXT_PROCEED_TIME] = self.get_format_time(self.scheduler.next_proceed_time)
        self.result_dict[KEY_ENABLE] = bool(self.scheduler.enable)

    @staticmethod
    def get_format_time(utc_date_time):
        try:
            if utc_date_time is None:
                return None

            time_zone = CURRENT_TIME_ZONE
            time_format = config.TIME_FORMAT.get('db_time_format')

            naive_time = timeUtil.get_naive_time_by_time(utc_date_time)

            local_date_time = timeUtil.utc_to_locale_time(naive_time, time_zone)
            str_time = timeUtil.date_time_to_time(local_date_time, time_format)
            return str_time
        except Exception as e:
            error_log(traceback.format_exc())
            raise e
