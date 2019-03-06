from RulesetComparer.b2bRequestTask.baseRequestTask import BaseRequestTask
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.logger import *


class DownloadRuleSetTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_RULE_SET_NAME = 'rulesetName'
    LOG_CLASS = "DownloadRuleSetTask"

    def __init__(self, environment_id, country_id, rule_set_name, compare_hash_key):
        BaseRequestTask.__init__(self)
        self.parse_data(environment_id, country_id)
        self.rule_set_name = rule_set_name
        self.file_name_with_path = get_rule_set_path(self.environment.name, self.country.name, compare_hash_key)
        self.request_data()

    def parse_data(self, environment_id, country_id):
        super().parse_data(environment_id, country_id)

    def request_data(self):
        super().request_data()

    def execute(self):
        request_params = [{"name": self.KEY_USER, "value": self.auth_data.get_account()},
                          {"name": self.KEY_PASSWORD, "value": self.auth_data.get_password()},
                          {"name": self.KEY_RULE_SET_NAME, "value": self.rule_set_name}]

        info_log(self.LOG_CLASS, '======== download rule set %s ========' % self.rule_set_name)
        response = self.client.service.exportRuleset(request_params)
        self.b2b_response_data = response

        if response.returnCode != 0:
            info_log(self.LOG_CLASS, "exportRuleset response loginId :" + str(response.loginId))
            info_log(self.LOG_CLASS, "exportRuleset error message :" + str(response.message))
            raise Exception(response.message[0].text)

        self.b2b_response_data = response
        self.save_file()

    def save_file(self):
        fileManager.create_folder(self.file_name_with_path)

        # save file
        payload = self.b2b_response_data.payload[
                  self.b2b_response_data.payload.index('<BRERuleList'):]
        fileManager.save_file(get_rule_set_full_file_name(self.file_name_with_path, self.rule_set_name), payload)

    def parse_result_data(self):
        return fileManager.load_file(self.file_name_with_path)

    def get_result_data(self):
        return super().get_result_data()
