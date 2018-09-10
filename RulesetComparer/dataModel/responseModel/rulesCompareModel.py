from RulesetComparer.dataModel.responseModel.responseModel import ResponseModel
from RulesetComparer.resource import apiResponse as api


class RulesCompareModel(ResponseModel):

    def __init__(self, rules_comparer):
        ResponseModel.__init__(self)
        if rules_comparer is None:
            self.set_error_code(api.STATUS_CODE_INVALID_PARAMETER)
        else:
            self.left_rules = rules_comparer.get_left_rules()
            self.right_rules = rules_comparer.get_right_rules()
            self.left_rules_list = rules_comparer.get_left_rules_list()
            self.right_rules_list = rules_comparer.get_right_rules_list()
            self.different = rules_comparer.get_different()

    def get_content_json(self):
        rules_compare_list = [self.get_rules_compared_json(self.left_rules, self.left_rules_list, self.different),
                              self.get_rules_compared_json(self.right_rules, self.right_rules_list, self.different)]
        return rules_compare_list

    def get_rules_compared_json(self, rules, only_list, different):
        if rules is None:
            self.error_code = api.STATUS_CODE_INVALID_PARAMETER

        rules_data = {
            api.RESPONSE_KEY_RULE_SET_NAME: rules.get_rules_name(),
            api.RESPONSE_KEY_RULE_STATUS_ADD:
                rules.get_rules_data_array_by_name_list(only_list),
            api.RESPONSE_KEY_RULE_STATUS_MODIFIED:
                rules.get_rules_data_array_by_name_list(different)
        }

        return rules_data



