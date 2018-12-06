import traceback
import RulesetComparer.properties.dataKey as key
from RulesetComparer.properties import config
from RulesetComparer.utils import timeUtil
from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer
from RulesetComparer.utils.logger import *


class ReportSchedulerInfoBuilder(BaseBuilder):

    def __init__(self, info_module):
        self.info_module = info_module
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        try:
            self.result_dict["task_id"] = self.info_module.id
            self.result_dict["base_environment_id"] = EnvironmentSerializer(self.info_module.base_environment).data
            self.result_dict["compare_environment_id"] = EnvironmentSerializer(
                self.info_module.compare_environment).data
            self.result_dict["module"] = self.get_module_data()
            self.result_dict["country_list"] = CountrySerializer(self.info_module.country_list, many=True).data
            self.result_dict["mail_list"] = self.get_mail_list()
            self.result_dict["interval_hour"] = self.info_module.interval_hour
            self.result_dict["last_proceed_time"] = self.get_format_time(self.info_module.last_proceed_time)
            self.result_dict["next_proceed_time"] = self.get_format_time(self.info_module.next_proceed_time)
            self.result_dict["status"] = self.get_status()

        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def get_module_data(self):
        try:
            module_map = {"id": self.info_module.module.id,
                          "name": self.info_module.module.name,
                          "icon_file_name": self.info_module.module.icon_file_name}
            return module_map
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def get_mail_list(self):
        try:
            return self.info_module.mail_list.split(",")
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    @staticmethod
    def get_format_time(date_time):
        try:
            if date_time is None:
                return None

            time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')
            format_time = timeUtil.date_time_to_time(date_time, time_format)
            return format_time
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def get_status(self):
        try:
            if self.info_module.enable == key.STATUS_ENABLE:
                return True
            else:
                return False
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())
