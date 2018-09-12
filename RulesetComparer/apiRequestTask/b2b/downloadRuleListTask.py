from RulesetComparer.apiRequestTask.b2b.baseRequestTask import BaseRequestTask
from RulesetComparer.properties import apiResponse
from RulesetComparer.utils.modelManager import get_single_model
from RulesetComparer.models import Environment
from RulesetComparer.dataModel.xml.ruleListModel import RuleListModel
from django.conf import settings
from zeep import Client


class DownloadRuleListTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_COUNTRY = 'ownerId'

    def __init__(self, environment, country):
        self.environment = environment
        self.country = country
        BaseRequestTask.__init__(self)

    def request_data(self):
        env_obj = get_single_model(Environment,
                                   environment=self.environment,
                                   country=self.country)
        if env_obj is None:
            self.error_code(apiResponse.STATUS_CODE_INVALID_PARAMETER)
            return

        self.add_request_parameter(self.KEY_USER, env_obj.userId)
        self.add_request_parameter(self.KEY_PASSWORD, env_obj.password)
        self.add_request_parameter(self.KEY_COUNTRY, self.country)

        print("call download_rule_set in service\n environment = %s , country = %s" % (self.environment, self.country))

        client = Client(settings.B2B_RULE_SET_CLIENT % env_obj.url)

        response = client.service.getOwnedBRERuleSets(self.request_parameter())
        self.b2b_response_data = response
        self.b2b_response_error_check()

    # for getting response content
    def get_content(self):
        if self.request_fail() is True:
            return []

        return self.get_content_json()

    # for getting response content to return json format
    def get_content_json(self):
        payload_data_encoding = self.b2b_response_data.payload.encode(settings.UNICODE_ENCODING)
        rule_list_model = RuleListModel(payload_data_encoding)

        return rule_list_model.get_rules_file_name_list()


