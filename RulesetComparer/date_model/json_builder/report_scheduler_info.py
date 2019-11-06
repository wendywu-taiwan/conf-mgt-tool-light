import traceback
import ast
from ConfigManageTool.settings import CURRENT_TIME_ZONE
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleBaseBuilder
from RulesetComparer.date_model.json_builder.mail_content_type import MailContentTypesBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.frequency_type import FrequencyTypeBuilder
from common.data_object.json_builder.module import ModuleBuilder


class ReportSchedulerInfoBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user, scheduler):
        self.scheduler = scheduler
        self.countries = self.scheduler.country_list.all()
        self.mail_content_types = self.scheduler.mail_content_type_list.all()
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        try:
            self.result_dict[KEY_TASK_ID] = self.scheduler.id
            self.result_dict["base_environment"] = EnvironmentBuilder(
                environment=self.scheduler.base_environment).get_data()
            self.result_dict["compare_environment"] = EnvironmentBuilder(
                environment=self.scheduler.compare_environment).get_data()
            self.result_dict[KEY_MODULE_DATA] = ModuleBuilder(self.scheduler.module).get_data()
            self.result_dict[KEY_COUNTRY_LIST] = CountriesBuilder(countries=self.countries).get_data()
            self.result_dict[RULESET_MAIL_CONTENT_TYPE] = MailContentTypesBuilder(self.mail_content_types).get_data()
            self.result_dict["mail_list"] = self.get_mail_list()
            self.result_dict[KEY_FREQUENCY_TYPE] = FrequencyTypeBuilder(self.scheduler.frequency_type).get_data()
            self.result_dict[KEY_INTERVAL] = self.scheduler.interval
            self.result_dict[KEY_LAST_PROCEED_TIME] = self.get_format_time(self.scheduler.last_proceed_time)
            self.result_dict[KEY_NEXT_PROCEED_TIME] = self.get_format_time(self.scheduler.next_proceed_time)
            self.result_dict[KEY_ENABLE] = bool(self.scheduler.enable)

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

            time_zone = CURRENT_TIME_ZONE
            time_format = config.TIME_FORMAT.get('db_time_format')

            naive_time = timeUtil.get_naive_time(utc_date_time.year, utc_date_time.month, utc_date_time.day,
                                                 utc_date_time.hour, utc_date_time.minute, utc_date_time.second)

            local_date_time = timeUtil.utc_to_locale_time(naive_time, time_zone)
            str_time = timeUtil.date_time_to_time(local_date_time, time_format)
            return str_time
        except Exception as e:
            error_log(traceback.format_exc())
            raise e


class ReportSchedulersBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user, schedulers):
        self.schedulers = schedulers
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        array = []
        for scheduler in self.schedulers:
            data = ReportSchedulerInfoBuilder(None, scheduler).get_data()
            array.append(data)
        self.result_dict[KEY_DATA] = array
