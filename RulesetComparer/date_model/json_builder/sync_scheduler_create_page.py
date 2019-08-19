from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleBaseBuilder
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.environment import EnvironmentsBuilder
from permission.models import Country, Environment
from RulesetComparer.properties.key import *
from RulesetComparer.properties.config import RULESET_SYNC_UP_ACTION


class SyncSchedulerCreatePageBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user):
        self.git_environment = Environment.objects.get(name=GIT_NAME)
        self.int2_environment = Environment.objects.get(name=INT2_NAME)
        self.countries = Country.objects.all()
        self.action_list = RULESET_SYNC_UP_ACTION
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[SOURCE_ENVIRONMENT] = EnvironmentsBuilder(environments=[self.git_environment]).get_data()
        self.result_dict[TARGET_ENVIRONMENT] = EnvironmentsBuilder(environments=[self.int2_environment]).get_data()
        self.result_dict[ENVIRONMENT_SELECT_COUNTRY] = CountriesBuilder(countries=self.countries).get_data()
        self.result_dict[ACTION_LIST] = self.action_list
