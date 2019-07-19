from RulesetComparer.task.baseRequestTask import BaseRequestTask
from RulesetComparer.date_model.xml.ruleSetObject import RulesetObject
from RulesetComparer.properties import dataKey
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.rulesetUtil import build_ruleset_xml
from RulesetComparer.date_model.json_builder.ruleset_b2b_action_result import RulesetB2BActionResultBuilder


class UpdateRulesetTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_COUNTRY = 'ownerId'
    LOG_CLASS = "UpdateRulesetTask"

    def __init__(self, target_environment, country, ruleset_name, source_xml, target_xml, diff_json):
        BaseRequestTask.__init__(self)
        self.ruleset_name = ruleset_name
        self.source_xml = source_xml
        self.target_xml = target_xml
        self.diff_json = diff_json
        self.parse_data(target_environment.id, country.id, dataKey.B2B_SERVICE_RULESET_ASSIGNMENT)
        self.request_data()

    def execute(self):
        info_log(self.LOG_CLASS, '======== update ruleset %s ========' % self.ruleset_name)
        source_only_rules = self.diff_json["source_env_only_rules"]["rules_array"]
        normal_rules = self.diff_json["normal_rules"]["rules_array"]
        different_rules = self.diff_json["different_rules"]["rules_array"]
        source_ruleset_map = RulesetObject(self.source_xml, self.ruleset_name).rulesMap
        target_ruleset_map = RulesetObject(self.target_xml, self.ruleset_name).rulesMap
        rule_model_list = list()

        # add normal rules from target env
        rule_model_list.extend(self.__get_rule_model_list__(normal_rules, target_ruleset_map))
        # add source only rules from source env
        rule_model_list.extend(self.__get_rule_model_list__(source_only_rules, source_ruleset_map))
        # add different rules from source env
        rule_model_list.extend(self.__get_rule_model_list__(different_rules, source_ruleset_map))

        ruleset_xml = build_ruleset_xml(rule_model_list)

        request_params = [{"name": "loginId", "value": self.auth_data.get_account()},
                          {"name": "password", "value": self.auth_data.get_password()},
                          {"name": "rulesetName", "value": self.ruleset_name}]

        response = self.client.service.importRuleset(request_params,
                                                     payload=ruleset_xml.replace('BRERuleListType', 'BRERuleList'))
        if response.returnCode != 0:
            info_log(self.LOG_CLASS, "update ruleset response loginId :" + str(response.loginId))
            info_log(self.LOG_CLASS, "update ruleset error message :" + str(response.message))
        self.b2b_response_data = response
        info_log(self.LOG_CLASS, '======== update ruleset finish ========')

    def parse_result_data(self):
        self.result_data = RulesetB2BActionResultBuilder(self.ruleset_name, dataKey.RULESET_UPDATE,
                                                         self.b2b_response_data).get_data()

    @staticmethod
    def __get_rule_model_list__(rule_key_array, rule_model_map):
        rule_model_list = list()
        for rule_key_obj in rule_key_array:
            rule_key = rule_key_obj["combined_key"]
            rule_model = rule_model_map.get(rule_key)
            if rule_model is None:
                print("rule model is none :" + rule_key)
            rule_model_list.append(rule_model)

        return rule_model_list
