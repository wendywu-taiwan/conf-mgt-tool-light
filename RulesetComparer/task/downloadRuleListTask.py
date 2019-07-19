from RulesetComparer.task.baseRequestTask import BaseRequestTask
from RulesetComparer.date_model.xml.ruleset_list import RuleListModel
from RulesetComparer.properties import key
from RulesetComparer.utils.logger import *


class DownloadRuleListTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_COUNTRY = 'ownerId'
    LOG_CLASS = "DownloadRuleListTask"

    def __init__(self, environment_id, country_id):
        BaseRequestTask.__init__(self)
        self.parse_data(environment_id, country_id, key.B2B_SERVICE_RULESET_ASSIGNMENT)
        self.request_data()

    def parse_data(self, environment_id, country_id, b2b_service_name):
        super().parse_data(environment_id, country_id, b2b_service_name)

    def request_data(self):
        super().request_data()

    def execute(self):
        info_log(self.LOG_CLASS, '======== download ruleset list ========')
        info_log(self.LOG_CLASS, "environment = %s , country = %s" % (self.environment, self.country))

        request_params = [{"name": self.KEY_USER, "value": self.auth_data.get_account()},
                          {"name": self.KEY_PASSWORD, "value": self.auth_data.get_password()},
                          {"name": self.KEY_COUNTRY, "value": self.country.name}]

        response = self.client.service.getOwnedBRERuleSets(request_params)
        if response.returnCode != 0:
            info_log(self.LOG_CLASS, "getOwnedBRERuleSets response loginId :" + str(response.loginId))
            info_log(self.LOG_CLASS, "getOwnedBRERuleSets error message :" + str(response.message))
            raise Exception(response.message[0].text)
        self.b2b_response_data = response
        info_log(self.LOG_CLASS, '======== download ruleset list finished ========')

    def parse_result_data(self):
        payload_data_encoding = self.b2b_response_data.payload.encode(settings.UNICODE_ENCODING)
        parser = RuleListModel(payload_data_encoding)
        self.result_data = parser.get_rules_file_name_list()

    def get_result_data(self):
        return super().get_result_data()
