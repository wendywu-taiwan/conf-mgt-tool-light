from RulesetComparer.utils.fileManager import *
from RulesetComparer.task.baseRequestTask import BaseRequestTask
from RulesetComparer.properties import dataKey
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.rulesetB2BActionResultBuilder import RulesetB2BActionResultBuilder
from RulesetComparer.properties.apiResponse import RESPONSE_EXPORT_RULESET_NOT_FOUND
from RulesetComparer.utils.timeUtil import get_current_timestamp


class DownloadRulesetTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_RULE_SET_NAME = 'rulesetName'
    LOG_CLASS = "DownloadRulesetTask"

    def __init__(self, environment_id, country_id, ruleset_name, compare_hash_key=None):
        BaseRequestTask.__init__(self)
        self.ruleset_name = ruleset_name
        self.result_builder = None
        if compare_hash_key is None:
            compare_hash_key = hash(get_current_timestamp())
        self.compare_hash_key = compare_hash_key
        self.ruleset_exist = True

        self.parse_data(environment_id, country_id, dataKey.B2B_SERVICE_RULESET_ASSIGNMENT)
        self.file_name_with_path = get_rule_set_path(self.environment.name, self.country.name, self.compare_hash_key)
        self.request_data()

    def request_data(self):
        return super().request_data()

    def execute(self):
        request_params = [{"name": self.KEY_USER, "value": self.auth_data.get_account()},
                          {"name": self.KEY_PASSWORD, "value": self.auth_data.get_password()},
                          {"name": self.KEY_RULE_SET_NAME, "value": self.ruleset_name}]

        info_log(self.LOG_CLASS, '======== download ruleset %s ========' % self.ruleset_name)
        response = self.client.service.exportRuleset(request_params)
        response_message = response.message[0]

        if response.returnCode != 0:
            info_log(self.LOG_CLASS, "exportRuleset response loginId :" + str(response.loginId))
            info_log(self.LOG_CLASS, "exportRuleset error message :" + str(response_message))

        if response_message.messageCode == RESPONSE_EXPORT_RULESET_NOT_FOUND:
            self.ruleset_exist = False

        if self.check_save_file():
            self.save_file(response, self.ruleset_name)

        self.b2b_response_data = response
        info_log(self.LOG_CLASS, '======== download ruleset finished ========')

    def parse_result_data(self):
        self.result_builder = RulesetB2BActionResultBuilder(self.ruleset_name, dataKey.RULESET_UPDATE,
                                                            self.b2b_response_data)
        self.success = self.result_builder.success
        self.result_data = self.result_builder.get_data()

    def get_ruleset_xml(self):
        return self.result_builder.get_payload_brerulelist()

    def get_result_data(self):
        return super().get_result_data()

    def check_save_file(self):
        if self.compare_hash_key is None or self.ruleset_exist is False:
            return False
        else:
            return True

    def save_file(self, response_xml, ruleset_name):
        info_log(self.LOG_CLASS, 'save file, path:' + self.file_name_with_path)
        create_folder(self.file_name_with_path)

        # save file
        payload = response_xml.payload[response_xml.payload.index('<BRERuleList'):]
        save_file(get_rule_set_full_file_name(self.file_name_with_path, ruleset_name), payload)
