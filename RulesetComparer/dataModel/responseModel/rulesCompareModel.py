from RulesetComparer.dataModel.responseModel.responseModel import ResponseModel
from RulesetComparer.properties import apiResponse as api


class RulesCompareModel(ResponseModel):

    def __init__(self, left_env, right_env, rule_set_name, comparer):
        ResponseModel.__init__(self)
        self.left_env = left_env
        self.right_env = right_env
        self.rule_set_name = rule_set_name
        if comparer is None:
            self.set_error_code(api.STATUS_CODE_INVALID_PARAMETER)
        else:
            self.comparer = comparer

    def get_content_json(self):

        rules_compare_list = list()
        rules_compare_list.append(self.get_rules_compared_json(self.left_env, self.comparer.get_left_rules_array())),
        rules_compare_list.append(self.get_rules_compared_json(self.right_env, self.comparer.get_right_rules_array())),

        dictionary = {
            api.RESPONSE_KEY_RULE_SET_NAME: self.rule_set_name,
            api.RESPONSE_KEY_ENVIRONMENT_LIST: rules_compare_list,
            api.RESPONSE_KEY_DIFF_LIST: self.comparer.get_difference_rules_array()
                      }
        return dictionary

    @staticmethod
    def get_rules_compared_json(environment, rules_array):
        rules_data = {
            api.RESPONSE_KEY_ENVIRONMENT_NAME: environment,
            api.RESPONSE_KEY_RULESET_FILE_LIST: rules_array
        }

        return rules_data



