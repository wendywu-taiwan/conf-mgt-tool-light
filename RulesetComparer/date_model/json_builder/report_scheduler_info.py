import traceback
import ast
import RulesetComparer.properties.key as key
from RulesetComparer.properties import config
from RulesetComparer.utils import timeUtil
from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, MailContentTypeSerializer
from RulesetComparer.utils.logger import *


class ReportSchedulerInfoBuilder(BaseBuilder):

    def __init__(self, scheduler):
        self.scheduler = scheduler
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        try:
            self.result_dict[KEY_TASK_ID] = self.scheduler.id
            self.result_dict["base_environment"] = EnvironmentSerializer(self.scheduler.base_environment).data
            self.result_dict["compare_environment"] = EnvironmentSerializer(
                self.scheduler.compare_environment).data
            self.result_dict["module"] = self.get_module_data()
            self.result_dict[KEY_COUNTRY_LIST] = CountrySerializer(self.scheduler.country_list, many=True).data
            self.result_dict[RULESET_MAIL_CONTENT_TYPE] = MailContentTypeSerializer(
                self.scheduler.mail_content_type_list, many=True).data
            self.result_dict["mail_list"] = self.get_mail_list()
            self.result_dict[KEY_INTERVAL_HOUR] = self.scheduler.interval_hour
            self.result_dict[KEY_LAST_PROCEED_TIME] = self.get_format_time(self.scheduler.last_proceed_time)
            self.result_dict[KEY_NEXT_PROCEED_TIME] = self.get_format_time(self.scheduler.next_proceed_time)
            self.result_dict[KEY_ENABLE] = bool(self.scheduler.enable)

        except Exception as e:
            error_log(traceback.format_exc())
            raise e

    def get_module_data(self):
        try:
            module_map = {"id": self.scheduler.module.id,
                          "name": self.scheduler.module.name,
                          "display_name": self.scheduler.module.display_name}
            return module_map
        except Exception as e:
            error_log(traceback.format_exc())
            raise e

    def get_mail_list(self):
        try:
            return ast.literal_eval(self.scheduler.mail_list)
        except Exception:
            return self.scheduler.mail_list

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
