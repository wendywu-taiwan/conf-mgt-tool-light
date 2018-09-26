from django.conf import settings
from zeep import Client

from RulesetComparer.b2bRequestTask.baseRequestTask import BaseRequestTask
from RulesetComparer.models import Environment, Country, B2BRuleSetServer
from RulesetComparer.properties import apiResponse
from RulesetComparer.utils import fileManager


class DownloadRuleSetTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_RULE_SET_NAME = 'rulesetName'

    def __init__(self, environment, country, rule_set_name, compare_hash_key):
        self.environment = environment
        self.country = country
        self.rule_set_name = rule_set_name
        self.download_status = apiResponse.RESPONSE_KEY_FAIL
        self.compare_hash_key = compare_hash_key
        self.file_name_with_path = None
        BaseRequestTask.__init__(self)

    def request_data(self):
        environment = Environment.objects.get(name=self.environment)
        country = Country.objects.get(name=self.country)
        b2b_service = B2BRuleSetServer.objects.get(country_id=country.id,
                                                   environment_id=environment.id)

        if b2b_service is None:
            self.error_code(apiResponse.STATUS_CODE_INVALID_PARAMETER)

        client = Client(settings.B2B_RULE_SET_CLIENT % b2b_service.url)

        self.add_request_parameter(self.KEY_USER, b2b_service.user_id)
        self.add_request_parameter(self.KEY_PASSWORD, b2b_service.password)
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
        save_file_path = settings.RULESET_SAVED_PATH % (self.environment,
                                                        self.country,
                                                        self.compare_hash_key)
        fileManager.create_folder(save_file_path)
        # save file
        self.file_name_with_path = settings.RULESET_SAVED_NAME % (save_file_path,
                                                                  self.rule_set_name)

        payload = self.b2b_response_data.payload[
                  self.b2b_response_data.payload.index('<BRERuleList'):]
        fileManager.save_file(self.file_name_with_path, payload)

    def get_rule_set_file(self):
        if self.request_fail():
            return None

        return fileManager.load_file(self.file_name_with_path)

