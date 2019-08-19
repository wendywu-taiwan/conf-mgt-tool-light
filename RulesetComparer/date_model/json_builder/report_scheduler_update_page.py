from RulesetComparer.date_model.json_builder.report_scheduler_info import ReportSchedulerInfoBuilder
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleBaseBuilder
from RulesetComparer.date_model.json_builder.mail_content_type import MailContentTypesBuilder
from common.data_object.json_builder.country import CountriesBuilder
from permission.models import Country
from RulesetComparer.models import MailContentType, ReportSchedulerInfo


class ReportSchedulerUpdatePageBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user, visible_data, scheduler_id):
        self.environment_data = visible_data
        self.country_data = CountriesBuilder(countries=Country.objects.all()).get_data()
        self.mail_content_types = MailContentTypesBuilder(MailContentType.objects.all()).get_data()
        self.scheduler = ReportSchedulerInfo.objects.get(id=scheduler_id)
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENTS] = self.environment_data
        self.result_dict[KEY_COUNTRIES] = self.country_data
        self.result_dict[RULESET_MAIL_CONTENT_TYPE] = self.mail_content_types
        self.result_dict[SCHEDULER_DATA] = ReportSchedulerInfoBuilder(None, self.scheduler).get_data()
