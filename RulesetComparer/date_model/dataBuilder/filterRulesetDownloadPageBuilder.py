from RulesetComparer.date_model.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.dataKey import *
from RulesetComparer.date_model.dataBuilder.environmentBuilder import EnvironmentBuilder
from RulesetComparer.date_model.dataBuilder.countryBuilder import CountryBuilder
from RulesetComparer.utils.stringFilter import array_filter


class FilterRulesetDownloadPageBuilder(BaseBuilder):
    def __init__(self, country, environment, filter_keys, ruleset_name_list):
        self.country = country
        self.environment = environment
        self.filter_keys = filter_keys
        self.ruleset_name_list = ruleset_name_list
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_COUNTRY] = CountryBuilder(self.country).get_data()
        self.result_dict[KEY_ENVIRONMENT] = EnvironmentBuilder(environment=self.environment).get_data()
        self.result_dict[RULE_NAME_LIST] = array_filter(self.ruleset_name_list, self.filter_keys)
