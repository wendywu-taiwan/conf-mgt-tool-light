from RulesetComparer.date_model.json_builder.report_scheduler_info import RulesetReportSchedulerBuilder
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleRulesetBuilder
from RulesetComparer.date_model.json_builder.mail_content_type import MailContentTypesBuilder
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.frequency_type import FrequencyTypesBuilder
from common.models import FrequencyType
from permission.models import Country
from RulesetComparer.models import MailContentType, ReportSchedulerInfo


class ReportSchedulerUpdatePageBuilder(AdminConsoleRulesetBuilder):

    def __init__(self, user, visible_data, scheduler_id):
        self.environment_data = visible_data
        self.country_data = CountriesBuilder(countries=Country.objects.all()).get_data()
        self.mail_content_types = MailContentTypesBuilder(MailContentType.objects.all()).get_data()
        self.frequency_types = FrequencyTypesBuilder(FrequencyType.objects.all()).get_data()
        self.scheduler = ReportSchedulerInfo.objects.get(id=scheduler_id)
        AdminConsoleRulesetBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENTS] = self.environment_data
        self.result_dict[KEY_COUNTRIES] = self.country_data
        self.result_dict[RULESET_MAIL_CONTENT_TYPE] = self.mail_content_types
        self.result_dict[KEY_FREQUENCY_TYPES] = self.frequency_types
        self.result_dict[SCHEDULER_DATA] = RulesetReportSchedulerBuilder(None, self.scheduler).get_data()
