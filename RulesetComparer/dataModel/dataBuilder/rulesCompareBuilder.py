from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties import apiResponse as api
from RulesetComparer.properties import dataKey as key


class RulesCompareModel(BaseBuilder):

    def __init__(self, base_env, compare_env, rule_set_name, comparer):
        self.base_env = base_env
        self.compare_env = compare_env
        self.rule_set_name = rule_set_name
        self.comparer = comparer
        BaseBuilder.__init__(self)

    def get_data(self):
        rules_compare_list = list()
        rules_compare_list.append(self.get_rules_compared_json(self.base_env, self.comparer.get_left_rules_array())),
        rules_compare_list.append(self.get_rules_compared_json(self.compare_env, self.comparer.get_right_rules_array())),

        base_env_data = self.get_rules_compared_json(self.base_env,
                                                     self.comparer.get_base_rules_array())
        compared_env_data = self.get_rules_compared_json(self.compare_env,
                                                         self.comparer.get_compared_rules_array())
        dictionary = {
            key.RULE_SET_NAME: self.rule_set_name,
            key.RULE_SET_BASE_ONLY_DATA: base_env_data,
            key.RULE_SET_COMPARED_ONLY_DATA: compared_env_data,
            key.RULE_SET_DIFF_DATA: self.comparer.get_difference_rules_array()
                      }
        return dictionary

    @staticmethod
    def get_rules_compared_json(environment, rules_array):
        rules_data = {
            api.RESPONSE_KEY_ENVIRONMENT_NAME: environment,
            api.RESPONSE_KEY_RULESET_FILE_LIST: rules_array
        }

        return rules_data



