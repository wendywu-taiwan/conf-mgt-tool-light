from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleBaseBuilder
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.environment import EnvironmentsBuilder
from common.data_object.json_builder.frequency_type import FrequencyTypesBuilder
from common.models import FrequencyType
from permission.models import Country, Environment
from RulesetComparer.properties.key import *
from RulesetComparer.properties.config import RULESET_SYNC_UP_ACTION


class SyncSchedulerCreatePageBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user, sync_from_environments, sync_to_environments):
        self.git_environment = Environment.objects.get(name=GIT_NAME)
        self.int2_environment = Environment.objects.get(name=INT2_NAME)
        self.countries = Country.objects.all()
        self.action_list = RULESET_SYNC_UP_ACTION
        self.frequency_types = FrequencyType.objects.all()
        self.sync_from_environments = sync_from_environments
        self.sync_to_environments = sync_to_environments
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[SOURCE_ENVIRONMENT] = EnvironmentsBuilder(ids=self.sync_from_environments).get_data()
        self.result_dict[TARGET_ENVIRONMENT] = EnvironmentsBuilder(ids=self.sync_to_environments).get_data()
        self.result_dict[ENVIRONMENT_SELECT_COUNTRY] = CountriesBuilder(countries=self.countries).get_data()
        self.result_dict[KEY_FREQUENCY_TYPES] = FrequencyTypesBuilder(self.frequency_types).get_data()
        self.result_dict[ACTION_LIST] = self.action_list
