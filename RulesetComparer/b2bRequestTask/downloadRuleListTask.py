import traceback
from RulesetComparer.b2bRequestTask.baseRequestTask import BaseRequestTask
from RulesetComparer.dataModel.xml.ruleSetFileListParser import RuleListModel
from RulesetComparer.models import Country, Environment
from RulesetComparer.dataModel.dataParser.authDataParser import AuthDataParser
from django.conf import settings
from zeep import Client
from RulesetComparer.utils.logger import *


class DownloadRuleListTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_COUNTRY = 'ownerId'

    def __init__(self, environment_id, country_id):
        self.environment_id = environment_id
        self.country_id = country_id
        BaseRequestTask.__init__(self)

    def request_data(self):
        try:
            country = Country.objects.get(id=self.country_id)
            environment = Environment.objects.get(id=self.environment_id)
            auth_data = AuthDataParser(environment.name)

            self.add_request_parameter(self.KEY_USER, auth_data.get_account())
            self.add_request_parameter(self.KEY_PASSWORD, auth_data.get_password())
            self.add_request_parameter(self.KEY_COUNTRY, country.name)

            logging.info("call download_rule_set in service\n environment = %s , country = %s" % (environment, country))
            logging.info("b2b_rule_set_client = %s" % environment.b2b_rule_set_client)
            print("call download_rule_set in service\n environment = %s , country = %s" % (environment, country))

            client = Client(environment.b2b_rule_set_client)

            response = client.service.getOwnedBRERuleSets(self.request_parameter())
            self.b2b_response_data = response
            self.b2b_response_error_check()
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())

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
