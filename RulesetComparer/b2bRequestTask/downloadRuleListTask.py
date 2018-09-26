from RulesetComparer.b2bRequestTask.baseRequestTask import BaseRequestTask
from RulesetComparer.properties import apiResponse
from RulesetComparer.dataModel.xml.ruleListModel import RuleListModel
from RulesetComparer.models import B2BRuleSetServer, Country, Environment
from django.conf import settings
from zeep import Client


class DownloadRuleListTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_COUNTRY = 'ownerId'

    def __init__(self, environment_id, country_id):
        self.environment_id = environment_id
        self.country_id = country_id
        BaseRequestTask.__init__(self)

    def request_data(self):
        b2b_server = B2BRuleSetServer.objects.get(country_id=self.country_id,
                                                  environment_id=self.environment_id)
        country = Country.objects.get(id=self.country_id)
        environment = Environment.objects.get(id=self.environment_id)

        if b2b_server is None:
            self.error_code(apiResponse.STATUS_CODE_INVALID_PARAMETER)
            return
        self.add_request_parameter(self.KEY_USER, b2b_server.user_id)
        self.add_request_parameter(self.KEY_PASSWORD, b2b_server.password)
        self.add_request_parameter(self.KEY_COUNTRY, country.name)

        print("call download_rule_set in service\n environment = %s , country = %s" % (environment,country))

        client = Client(settings.B2B_RULE_SET_CLIENT % b2b_server.url)

        response = client.service.getOwnedBRERuleSets(self.request_parameter())
        self.b2b_response_data = response
        self.b2b_response_error_check()

    def get_rule_list(self):
        if self.request_fail() is True:
            return []

        payload_data_encoding = self.b2b_response_data.payload.encode(settings.UNICODE_ENCODING)
        rule_list_xml_parser = RuleListModel(payload_data_encoding)

        return rule_list_xml_parser.get_rules_file_name_list()

    # for getting response content
    def get_content(self):
        if self.request_fail() is True:
            return []

        return self.get_content_json()

    # for getting response content to return json format
    def get_content_json(self):
        payload_data_encoding = self.b2b_response_data.payload.encode(settings.UNICODE_ENCODING)
        rule_list_xml_parser = RuleListModel(payload_data_encoding)

        return rule_list_xml_parser.get_rules_file_name_list()


