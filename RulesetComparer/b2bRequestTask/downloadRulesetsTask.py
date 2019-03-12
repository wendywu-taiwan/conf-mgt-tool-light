from RulesetComparer.b2bRequestTask.baseRequestTask import BaseRequestTask
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.logger import *
from RulesetComparer.properties import dataKey


class DownloadRulesetsTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_RULE_SET_NAME = 'rulesetName'
    LOG_CLASS = "DownloadRuleSetTask"

    def __init__(self, environment_id, country_id, ruleset_list, compare_hash_key):
        BaseRequestTask.__init__(self)
        self.parse_data(environment_id, country_id, dataKey.B2B_SERVICE_RULESET_ASSIGNMENT)
        self.ruleset_list = ruleset_list
        self.file_name_with_path = get_rule_set_path(self.environment.name, self.country.name, compare_hash_key)
        self.request_data()

    def parse_data(self, environment_id, country_id, b2b_service_name):
        super().parse_data(environment_id, country_id, b2b_service_name)

    def request_data(self):
        super().request_data()

    def execute(self):
        for ruleset_name in self.ruleset_list:
            request_params = [{"name": self.KEY_USER, "value": self.auth_data.get_account()},
                              {"name": self.KEY_PASSWORD, "value": self.auth_data.get_password()},
                              {"name": self.KEY_RULE_SET_NAME, "value": ruleset_name}]

            info_log(self.LOG_CLASS, '======== download rule set %s ========' % ruleset_name)
            response = self.client.service.exportRuleset(request_params)

            if response.returnCode != 0:
                info_log(self.LOG_CLASS, "exportRuleset response loginId :" + str(response.loginId))
                info_log(self.LOG_CLASS, "exportRuleset error message :" + str(response.message))
                raise Exception(response.message[0].text)

            self.save_file(response, ruleset_name)

    def save_file(self, response_xml, ruleset_name):
        fileManager.create_folder(self.file_name_with_path)

        # save file
        payload = response_xml.payload[response_xml.payload.index('<BRERuleList'):]
        fileManager.save_file(get_rule_set_full_file_name(self.file_name_with_path, ruleset_name), payload)

    def parse_result_data(self):
        return self.ruleset_list

    def get_result_data(self):
        return super().get_result_data()
