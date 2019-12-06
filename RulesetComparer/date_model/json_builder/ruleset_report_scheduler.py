from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleRulesetBuilder
from RulesetComparer.date_model.json_builder.mail_content_type import MailContentTypesBuilder
from RulesetComparer.properties.key import KEY_MODULE_DATA, KEY_COUNTRY_LIST, RULESET_MAIL_CONTENT_TYPE, KEY_DATA
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.module import ModuleBuilder
from common.data_object.json_builder.report_scheduler import ReportSchedulerBuilder


class RulesetReportSchedulerBuilder(ReportSchedulerBuilder, AdminConsoleRulesetBuilder):
    def __init__(self, user, scheduler):
        ReportSchedulerBuilder.__init__(self, scheduler)
        AdminConsoleRulesetBuilder.__init__(self, user)
        self.countries = self.scheduler.country_list.all()
        self.mail_content_types = self.scheduler.mail_content_type_list.all()

    def __generate_data__(self):
        ReportSchedulerBuilder.__generate_data__(self)

    def get_report_data(self):
        self.result_dict["base_environment"] = EnvironmentBuilder(
            environment=self.scheduler.base_environment).get_data()
        self.result_dict["compare_environment"] = EnvironmentBuilder(
            environment=self.scheduler.compare_environment).get_data()
        self.result_dict[KEY_MODULE_DATA] = ModuleBuilder(self.scheduler.module).get_data()
        self.result_dict[KEY_COUNTRY_LIST] = CountriesBuilder(countries=self.countries).get_data()
        self.result_dict[RULESET_MAIL_CONTENT_TYPE] = MailContentTypesBuilder(self.mail_content_types).get_data()
        return self.result_dict

    def get_data(self):
        self.result_dict = AdminConsoleRulesetBuilder.get_data(self)
        self.result_dict = self.get_report_data()
        return self.result_dict


class RulesetReportSchedulersBuilder(AdminConsoleRulesetBuilder):
    def __init__(self, user, schedulers):
        self.schedulers = schedulers
        AdminConsoleRulesetBuilder.__init__(self, user)

    def __generate_data__(self):
        AdminConsoleRulesetBuilder.__generate_data__(self)

    def get_data(self):
        array = []
        for scheduler in self.schedulers:
            data = RulesetReportSchedulerBuilder(self.user, scheduler).get_report_data()
            array.append(data)
        self.result_dict[KEY_DATA] = array
        return AdminConsoleRulesetBuilder.get_data(self)