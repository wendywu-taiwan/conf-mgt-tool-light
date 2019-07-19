from RulesetComparer.task.baseRequestTask import BaseRequestTask
from RulesetComparer.properties import key
from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.ruleset_b2b_action_result import RulesetB2BActionResultBuilder


class ClearRulesetTask(BaseRequestTask):
    LOG_CLASS = "ClearRulesetTask"

    def __init__(self, target_environment, country, ruleset_name):
        BaseRequestTask.__init__(self)
        self.ruleset_name = ruleset_name
        self.parse_data(target_environment.id, country.id, key.B2B_SERVICE_RULESET_ASSIGNMENT)
        self.request_data()

    def parse_data(self, environment_id, country_id, b2b_service_name):
        super().parse_data(environment_id, country_id, b2b_service_name)

    def request_data(self):
        super().request_data()

    def execute(self):
        info_log(self.LOG_CLASS, '======== clear ruleset %s ========' % self.ruleset_name)
        info_log(self.LOG_CLASS, "environment = %s , country = %s" % (self.environment, self.country))

        request_params = [{"name": "loginId", "value": self.auth_data.get_account()},
                          {"name": "password", "value": self.auth_data.get_password()},
                          {"name": "rulesetName", "value": self.ruleset_name}]

        response = self.client.service.clearRuleset(request_params)
        if response.returnCode != 0:
            info_log(self.LOG_CLASS, "clear ruleset response loginId :" + str(response.loginId))
            info_log(self.LOG_CLASS, "clear ruleset error message :" + str(response.message))
        self.b2b_response_data = response
        info_log(self.LOG_CLASS, '======== clear ruleset finish ========')

    def parse_result_data(self):
        builder = RulesetB2BActionResultBuilder(self.ruleset_name, key.RULESET_CLEAR, self.b2b_response_data)
        self.result_data = builder.get_data()
        self.success = builder.success

    def get_result_data(self):
        return super().get_result_data()
