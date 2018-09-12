from RulesetComparer.apiRequestTask.b2b.baseRequestTask import BaseRequestTask
from RulesetComparer.utils.modelManager import get_single_model
from RulesetComparer.models import Environment
from RulesetComparer.properties import apiResponse
from django.conf import settings
from zeep import Client
from RulesetComparer.utils import fileManager


class DownloadRuleSetTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_RULE_SET_NAME = 'rulesetName'

    def __init__(self, environment, country, rule_set_name):
        self.environment = environment
        self.country = country
        self.rule_set_name = rule_set_name
        self.download_status = apiResponse.RESPONSE_KEY_FAIL
        BaseRequestTask.__init__(self)

    def request_data(self):
        env_obj = get_single_model(Environment, environment=self.environment, country=self.country)

        if env_obj is None:
            self.error_code(apiResponse.STATUS_CODE_INVALID_PARAMETER)

        client = Client(settings.B2B_RULE_SET_CLIENT % env_obj.url)

        self.add_request_parameter(self.KEY_USER, env_obj.userId)
        self.add_request_parameter(self.KEY_PASSWORD, env_obj.password)
        self.add_request_parameter(self.KEY_RULE_SET_NAME, self.rule_set_name)

        print('======== download rule set %s ========' % self.rule_set_name)
        response = client.service.exportRuleset(self.request_parameter())
        self.b2b_response_data = response
        self.b2b_response_error_check()

        if self.request_fail() is False:
            self.download_status = apiResponse.RESPONSE_KEY_SUCCESS

    def get_content(self):
        if self.request_fail():
            return None
        else:
            return self.rule_set_name

    def get_content_json(self):
        return {apiResponse.DATA_KEY_RULES_NAME: self.rule_set_name,
                apiResponse.DATA_KEY_DOWNLOAD_STATUS: self.download_status}

    def save_rule_set(self, file_name_with_path):
        if self.request_fail():
            return

        payload = self.b2b_response_data.payload[
                  self.b2b_response_data.payload.index('<BRERuleList'):]
        fileManager.save_file(file_name_with_path, payload)

