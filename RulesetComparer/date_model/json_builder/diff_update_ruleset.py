from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties.dataKey import *


class DiffUpdateRulesetBuilder(BaseBuilder):

    def __init__(self, ruleset_comparer):
        self.comparer = ruleset_comparer
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_NAME] = self.comparer.ruleset_name
        self.result_dict[KEY_SOURCE_ENV_ONLY_RULES] = self.generate_rules_data(self.comparer.get_source_rules_array())
        self.result_dict[KEY_TARGET_ENV_ONLY_RULES] = self.generate_rules_data(self.comparer.get_target_rules_array())
        self.result_dict[KEY_NORMAL_RULES] = self.generate_rules_data(self.comparer.get_normal_rules_array())
        self.result_dict[KEY_DIFFERENT_RULES] = self.generate_rules_data(self.comparer.get_difference_rules_array())

    def get_data(self):
        return self.result_dict

    @staticmethod
    def generate_rules_data(keys_array):
        data = {KEY_COUNT: len(keys_array), KEY_RULES_ARRAY: keys_array}
        return data
