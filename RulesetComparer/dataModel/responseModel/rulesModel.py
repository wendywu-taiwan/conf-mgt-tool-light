from RulesetComparer.dataModel.responseModel.responseModel import ResponseModel
from RulesetComparer.properties import apiResponse as api


class RulesModel(ResponseModel):

    def __init__(self, rules_module):
        ResponseModel.__init__(self)
        self.rules_module = rules_module
        if rules_module is None:
            self.set_error_code(api.STATUS_CODE_INVALID_PARAMETER)
        self.rules_map = rules_module.get_rules_map

    def get_content_json(self):
        return {api.RESPONSE_KEY_RULE_SET_NAME: self.rules_module.get_rules_name(),
                api.RESPONSE_KEY_RULE_SET_ARRAY: self.rules_module.get_rules_data_array()}

