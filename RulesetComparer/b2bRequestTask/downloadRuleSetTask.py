from django.conf import settings
from zeep import Client

from RulesetComparer.properties.config import get_rule_set_path
from RulesetComparer.b2bRequestTask.baseRequestTask import BaseRequestTask
from RulesetComparer.models import Country, Environment
from RulesetComparer.properties import apiResponse
from RulesetComparer.properties.config import get_rule_set_full_file_name
from RulesetComparer.utils import fileManager


class DownloadRuleSetTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_RULE_SET_NAME = 'rulesetName'

    def __init__(self, env_id, country_id, rule_set_name, compare_hash_key):
        self.environment = Environment.objects.get(id=env_id)
        self.country = Country.objects.get(id=country_id)
        self.rule_set_name = rule_set_name
        self.download_status = apiResponse.RESPONSE_KEY_FAIL
        self.compare_hash_key = compare_hash_key
        self.file_name_with_path = None
        BaseRequestTask.__init__(self)

    def request_data(self):
        client = Client(self.environment.b2b_rule_set_client)

        self.add_request_parameter(self.KEY_USER, self.environment.account)
        self.add_request_parameter(self.KEY_PASSWORD, self.environment.password)
        self.add_request_parameter(self.KEY_RULE_SET_NAME, self.rule_set_name)

        print('======== download rule set %s ========' % self.rule_set_name)
        response = client.service.exportRuleset(self.request_parameter())
        self.b2b_response_data = response
        self.b2b_response_error_check()

        if self.request_fail() is False:
            self.download_status = apiResponse.RESPONSE_KEY_SUCCESS
            self.save_rule_set()

    def get_content(self):
        if self.request_fail():
            return None
        else:
            return self.rule_set_name

    def get_content_json(self):
        return {apiResponse.DATA_KEY_RULES_NAME: self.rule_set_name,
                apiResponse.DATA_KEY_DOWNLOAD_STATUS: self.download_status}

    def save_rule_set(self):
        if self.request_fail():
            return

        # save file to specific path
        save_file_path = get_rule_set_path(self.environment.name,
                                           self.country.name,
                                           self.compare_hash_key)
        fileManager.create_folder(save_file_path)
        # save file

        payload = self.b2b_response_data.payload[
                  self.b2b_response_data.payload.index('<BRERuleList'):]
        fileManager.save_file(get_rule_set_full_file_name(save_file_path, self.rule_set_name),
                              payload)

    def get_rule_set_file(self):
        if self.request_fail():
            return None

        return fileManager.load_file(self.file_name_with_path)
