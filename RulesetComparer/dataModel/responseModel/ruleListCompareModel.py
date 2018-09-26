from RulesetComparer.dataModel.responseModel.responseModel import ResponseModel
from RulesetComparer.properties import apiResponse as api


class RuleListCompareModel(ResponseModel):

    def __init__(self, left_env_name, right_env_name, rule_file_list_comparer):
        ResponseModel.__init__(self)
        if rule_file_list_comparer is None:
            self.set_error_code(api.STATUS_CODE_INVALID_PARAMETER)
        else:
            self.left_env_name = left_env_name
            self.right_env_name = right_env_name
            self.left_list = rule_file_list_comparer.get_left_rules_list()
            self.right_list = rule_file_list_comparer.get_right_rules_list()
            self.union_list = rule_file_list_comparer.get_union_list()

    def get_content_json(self):
        if self.error_code is not None:
            return {}

        env_list = list()
        env_list.append(self.get_environment_object(self.left_env_name, self.left_list))
        env_list.append(self.get_environment_object(self.right_env_name, self.right_list))
        dict = {
            api.RESPONSE_KEY_ENVIRONMENT_LIST: env_list,
            api.RESPONSE_KEY_UNION_FILE_LIST: self.union_list
        }
        return dict

    @staticmethod
    def get_environment_object(env_name, rule_file_list):
        dict = {
            api.RESPONSE_KEY_ENVIRONMENT_NAME: env_name,
            api.RESPONSE_KEY_RULESET_FILE_LIST: rule_file_list
        }
        return dict



