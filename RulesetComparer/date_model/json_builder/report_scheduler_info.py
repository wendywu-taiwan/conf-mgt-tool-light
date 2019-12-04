import traceback
import ast
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleRulesetBuilder, \
    AdminConsoleSharedStorageBuilder
from RulesetComparer.date_model.json_builder.mail_content_type import MailContentTypesBuilder
from common.data_object.json_builder.base import BaseBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.frequency_type import FrequencyTypeBuilder
from common.data_object.json_builder.module import ModuleBuilder


class ReportSchedulerBuilder(BaseBuilder):

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.countries = self.scheduler.country_list.all()
        self.mail_content_types = self.scheduler.mail_content_type_list.all()
        BaseBuilder.__init__(self)

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

            naive_time = timeUtil.get_naive_time_by_time(utc_date_time)

            local_date_time = timeUtil.utc_to_locale_time(naive_time, time_zone)
            str_time = timeUtil.date_time_to_time(local_date_time, time_format)
            return str_time
        except Exception as e:
            error_log(traceback.format_exc())
            raise e


class ReportSchedulersBuilder(BaseBuilder):

    def __init__(self, schedulers):
        self.schedulers = schedulers
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        array = []
        for scheduler in self.schedulers:
            data = ReportSchedulerBuilder(scheduler).get_data()
            array.append(data)
        self.result_dict[KEY_DATA] = array


class RulesetReportSchedulerBuilder(ReportSchedulerBuilder, AdminConsoleRulesetBuilder):
    def __init__(self, user, scheduler):
        ReportSchedulerBuilder.__init__(self, scheduler)
        AdminConsoleRulesetBuilder.__init__(self, user)

    def __generate_data__(self):
        ReportSchedulerBuilder.__generate_data__(self)

    def get_data(self):
        return AdminConsoleRulesetBuilder.get_data(self)


class RulesetReportSchedulersBuilder(ReportSchedulersBuilder, AdminConsoleRulesetBuilder):
    def __init__(self, user, schedulers):
        ReportSchedulersBuilder.__init__(self, schedulers)
        AdminConsoleRulesetBuilder.__init__(self, user)

    def __generate_data__(self):
        ReportSchedulersBuilder.__generate_data__(self)

    def get_data(self):
        return AdminConsoleRulesetBuilder.get_data(self)


class SharedStorageReportSchedulerBuilder(ReportSchedulerBuilder, AdminConsoleSharedStorageBuilder):
    def __init__(self, user, scheduler):
        ReportSchedulerBuilder.__init__(self, scheduler)
        AdminConsoleSharedStorageBuilder.__init__(self, user)

    def __generate_data__(self):
        ReportSchedulerBuilder.__generate_data__(self)

    def get_data(self):
        return AdminConsoleSharedStorageBuilder.get_data(self)


class SharedStorageSchedulersBuilder(ReportSchedulersBuilder, AdminConsoleSharedStorageBuilder):
    def __init__(self, user, schedulers):
        ReportSchedulersBuilder.__init__(self, schedulers)
        AdminConsoleSharedStorageBuilder.__init__(self, user)

    def __generate_data__(self):
        ReportSchedulersBuilder.__generate_data__(self)

    def get_data(self):
        return AdminConsoleSharedStorageBuilder.get_data(self)

# class ReportSchedulerInfoBuilder(AdminConsoleRulesetBuilder):
#
#     def __init__(self, user, scheduler):
#         self.scheduler = scheduler
#         self.countries = self.scheduler.country_list.all()
#         self.mail_content_types = self.scheduler.mail_content_type_list.all()
#         AdminConsoleRulesetBuilder.__init__(self, user)
#
#     def __generate_data__(self):
#         try:
#             self.result_dict[KEY_TASK_ID] = self.scheduler.id
#             self.result_dict["base_environment"] = EnvironmentBuilder(
#                 environment=self.scheduler.base_environment).get_data()
#             self.result_dict["compare_environment"] = EnvironmentBuilder(
#                 environment=self.scheduler.compare_environment).get_data()
#             self.result_dict[KEY_MODULE_DATA] = ModuleBuilder(self.scheduler.module).get_data()
#             self.result_dict[KEY_COUNTRY_LIST] = CountriesBuilder(countries=self.countries).get_data()
#             self.result_dict[RULESET_MAIL_CONTENT_TYPE] = MailContentTypesBuilder(self.mail_content_types).get_data()
#             self.result_dict["mail_list"] = self.get_mail_list()
#             self.result_dict[KEY_FREQUENCY_TYPE] = FrequencyTypeBuilder(self.scheduler.frequency_type).get_data()
#             self.result_dict[KEY_INTERVAL] = self.scheduler.interval
#             self.result_dict[KEY_LAST_PROCEED_TIME] = self.get_format_time(self.scheduler.last_proceed_time)
#             self.result_dict[KEY_NEXT_PROCEED_TIME] = self.get_format_time(self.scheduler.next_proceed_time)
#             self.result_dict[KEY_ENABLE] = bool(self.scheduler.enable)
#
#         except Exception as e:
#             error_log(traceback.format_exc())
#             raise e
#
#     def get_mail_list(self):
#         try:
#             return ast.literal_eval(self.scheduler.mail_list)
#         except Exception:
#             return self.scheduler.mail_list
#
#     @staticmethod
#     def get_format_time(utc_date_time):
#         try:
#             if utc_date_time is None:
#                 return None
#
#             time_zone = CURRENT_TIME_ZONE
#             time_format = config.TIME_FORMAT.get('db_time_format')
#
#             naive_time = timeUtil.get_naive_time_by_time(utc_date_time)
#
#             local_date_time = timeUtil.utc_to_locale_time(naive_time, time_zone)
#             str_time = timeUtil.date_time_to_time(local_date_time, time_format)
#             return str_time
#         except Exception as e:
#             error_log(traceback.format_exc())
#             raise e


# class ReportSchedulersBuilder(AdminConsoleRulesetBuilder):
#
#     def __init__(self, user, schedulers):
#         self.schedulers = schedulers
#         AdminConsoleRulesetBuilder.__init__(self, user)
#
#     def __generate_data__(self):
#         array = []
#         for scheduler in self.schedulers:
#             data = ReportSchedulerInfoBuilder(None, scheduler).get_data()
#             array.append(data)
#         self.result_dict[KEY_DATA] = array
