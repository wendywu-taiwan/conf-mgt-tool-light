from RulesetComparer.date_model.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.dataKey import *
from RulesetComparer.date_model.dataBuilder.environmentBuilder import EnvironmentBuilder
from RulesetComparer.date_model.dataBuilder.countryBuilder import CountryBuilder


class RulesetDetailBuilder(BaseBuilder):
    def __init__(self, ruleset_loader):
        self.ruleset_list = ruleset_loader.ruleset_model.get_rules_data_array()
        self.environment = ruleset_loader.environment
        self.country = ruleset_loader.country
        self.ruleset_name = ruleset_loader.ruleset_name
        self.ruleset = ruleset_loader.get_ruleset()
        self.ruleset_path_info = ruleset_loader.ruleset_path_info

        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENT] = EnvironmentBuilder(environment=self.environment).get_data()
        self.result_dict[KEY_COUNTRY] = CountryBuilder(self.country).get_data()
        self.result_dict[KEY_RULESET_NAME] = self.ruleset_name
        self.result_dict[KEY_RULESET_DATA] = self.ruleset_list
        self.result_dict[KEY_RULESET_PATH_INFO] = self.ruleset_path_info
