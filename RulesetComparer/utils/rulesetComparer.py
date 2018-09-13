from RulesetComparer.dataModel.xml.rulesModel import RulesModel

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
            left_value = self.left_rules.get_rule_value(rule_key)
            right_value = self.right_rules.get_rule_value(rule_key)
            if left_value != right_value:
                self.different.append(rule_key)

    def get_left_rules(self):
        return self.left_rules

    def get_right_rules(self):
        return self.right_rules

    def get_left_rules_list(self):
        return self.leftKeyOnly

    def get_right_rules_list(self):
        return self.rightKeyOnly

    def get_different(self):
        return self.different




