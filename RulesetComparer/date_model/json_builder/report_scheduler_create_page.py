from RulesetComparer.date_model.json_builder.mail_content_type import MailContentTypesBuilder
from RulesetComparer.models import MailContentType
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleBaseBuilder
from common.data_object.json_builder.country import CountriesBuilder
from permission.models import Country


class ReportSchedulerCreatePageBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user, visible_data):
        self.environment_data = visible_data
        self.country_data = CountriesBuilder(countries=Country.objects.all()).get_data()
        self.mail_content_types = MailContentTypesBuilder(MailContentType.objects.all()).get_data()
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENTS] = self.environment_data
        self.result_dict[KEY_COUNTRIES] = self.country_data
        self.result_dict[RULESET_MAIL_CONTENT_TYPE] = self.mail_content_types
