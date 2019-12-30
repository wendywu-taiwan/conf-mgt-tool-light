from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from common.data_object.json_builder.country import CountryBuilder
from common.utils.utility import parse_db_string_list


class ReportSchedulerSkipRulesetBuilder(BaseBuilder):

    def __init__(self, skip_ruleset_model):
        try:
            self.skip_ruleset_model = skip_ruleset_model
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_COUNTRY] = CountryBuilder(self.skip_ruleset_model.country).get_data()
        self.result_dict[KEY_RULESET_LIST] = parse_db_string_list(self.skip_ruleset_model.ruleset_list)


class ReportSchedulerSkipRulesetsBuilder(BaseBuilder):

    def __init__(self, skip_ruleset_models):
        try:
            self.skip_ruleset_models = skip_ruleset_models
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.parse_skip_rulesets()

    def parse_skip_rulesets(self):
        array = []
        for skip_ruleset in self.skip_ruleset_models:
            data = ReportSchedulerSkipRulesetBuilder(skip_ruleset).get_data()
            array.append(data)
        return array
