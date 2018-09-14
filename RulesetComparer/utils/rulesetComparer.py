from RulesetComparer.dataModel.xml.rulesModel import RulesModel
from RulesetComparer.properties import apiResponse as apiKey


class RulesetComparer:
    def __init__(self, left_rules, right_rules):
        self.left_rules = left_rules
        self.right_rules = right_rules
        self.leftKeyOnly = []
        self.rightKeyOnly = []
        self.different = []
        self.classify_rule_keys()

    def classify_rule_keys(self):
        left_key_set = set(self.left_rules.get_rules_name_list())
        right_key_set = set(self.right_rules.get_rules_name_list())

        # get rule key only in left rules
        self.leftKeyOnly = list(left_key_set - right_key_set)
        # get rule key only in right rules
        self.rightKeyOnly = list(right_key_set - left_key_set)

        # get union key in two rules
        tmp = list(left_key_set & right_key_set)
        for rule_key in tmp:
            left_value = self.left_rules.get_rule_full_value(rule_key)
            right_value = self.right_rules.get_rule_full_value(rule_key)
            if left_value != right_value:
                self.different.append(rule_key)

    def get_left_rules_array(self):
        return self.left_rules.get_rules_data_array(self.leftKeyOnly)

    def get_right_rules_array(self):
        return self.right_rules.get_rules_data_array(self.rightKeyOnly)

    def get_difference_rules_array(self):
        data_array = self.left_rules.get_rules_data_array(self.different)
        for rule in data_array:
            rule_value_list = list()
            rule_expression_list = list()
            rule_key = rule[apiKey.RESPONSE_KEY_RULE_KEY]
            rule_value_list.append(self.left_rules.get_rule_value(rule_key))
            rule_value_list.append(self.right_rules.get_rule_value(rule_key))
            rule_expression_list.append(self.left_rules.get_rule_expression(rule_key))
            rule_expression_list.append(self.right_rules.get_rule_expression(rule_key))

            if len(rule_value_list) != 0:
                rule[apiKey.RESPONSE_KEY_RULE_VALUE] = rule_value_list

            if len(rule_expression_list) != 0:
                rule[apiKey.RESPONSE_KEY_RULE_EXPRESSION] = rule_expression_list

        return data_array
