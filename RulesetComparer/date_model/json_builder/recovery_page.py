from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleRulesetBuilder
from common.data_object.json_builder.environment import EnvironmentsBuilder
from common.data_object.json_builder.country import CountriesBuilder


class RecoveryPageFilterEnvironmentsBuilder(AdminConsoleRulesetBuilder):

    def __init__(self, user, environment_ids):
        self.environment_ids = environment_ids
        AdminConsoleRulesetBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENTS] = EnvironmentsBuilder(ids=self.environment_ids).get_data()


class RecoveryPageFilterCountriesBuilder(AdminConsoleRulesetBuilder):
    def __init__(self, user, country_ids):
        self.country_ids = country_ids
        AdminConsoleRulesetBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[KEY_COUNTRIES] = CountriesBuilder(ids=self.country_ids).get_data()
