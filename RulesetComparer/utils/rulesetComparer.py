from RulesetComparer.dataModel.xml.rulesModel import RulesModel
from RulesetComparer.properties import apiResponse as apiKey


class RulesetComparer:
    def __init__(self, base_rules, compare_rules):
        self.base_rules = base_rules
        self.compare_rules = compare_rules
        self.baseKeyOnly = []
        self.compareKeyOnly = []
        self.different = []
        self.classify_rule_keys()

    def classify_rule_keys(self):
        base_key_set = set(self.base_rules.get_rules_name_list())
        compare_key_set = set(self.compare_rules.get_rules_name_list())

        # get rule key only in left rules
        self.baseKeyOnly = list(base_key_set - compare_key_set)
        # get rule key only in right rules
        self.compareKeyOnly = list(compare_key_set - base_key_set)

        # get union key in two rules
        tmp = list(base_key_set & compare_key_set)
        for rule_key in tmp:
            left_value = self.base_rules.get_rule_full_value(rule_key)
            right_value = self.compare_rules.get_rule_full_value(rule_key)
            if left_value != right_value:
                self.different.append(rule_key)

    def no_difference(self):
        if len(self.baseKeyOnly) == 0 and len(self.compareKeyOnly) == 0 and len(self.different) == 0:
            return True
        return False

    def get_base_key_count(self):
        return len(self.baseKeyOnly)

    def get_compare_key_count(self):
        return len(self.compareKeyOnly)

    def get_difference_count(self):
        return len(self.different)

    def get_left_rules_array(self):
        return self.base_rules.get_rules_data_array(self.baseKeyOnly)

    def get_right_rules_array(self):
        return self.compare_rules.get_rules_data_array(self.compareKeyOnly)

    def get_difference_rules_array(self):
        data_array = self.base_rules.get_rules_data_array(self.different)
        for rule in data_array:
            rule_value_list = list()
            rule_expression_list = list()
            rule_key = rule[apiKey.RESPONSE_KEY_RULE_KEY]
            rule_value_list.append(self.base_rules.get_rule_value(rule_key))
            rule_value_list.append(self.compare_rules.get_rule_value(rule_key))
            rule_expression_list.append(self.base_rules.get_rule_expression(rule_key))
            rule_expression_list.append(self.compare_rules.get_rule_expression(rule_key))

            if len(rule_value_list) != 0:
                rule[apiKey.RESPONSE_KEY_RULE_VALUE] = rule_value_list

            if len(rule_expression_list) != 0:
                rule[apiKey.RESPONSE_KEY_RULE_EXPRESSION] = rule_expression_list

        return data_array
