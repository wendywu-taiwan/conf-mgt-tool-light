

class RuleListComparer:
    def __init__(self, left_rule_list, right_rule_list):
        self.left_rule_list = left_rule_list
        self.right_rule_list = right_rule_list
        self.leftOnly = []
        self.rightOnly = []
        self.union = []
        self.classify_rule_list()

    def classify_rule_list(self):
        left_key_set = set(self.left_rule_list)
        right_key_set = set(self.right_rule_list)

        # get rule key only in left rules
        self.leftOnly = list(left_key_set - right_key_set)
        # get rule key only in right rules
        self.rightOnly = list(right_key_set - left_key_set)

        # get union key in two rules
        self.union = list(left_key_set & right_key_set)

    def get_left_rules_list(self):
        return self.leftOnly

    def get_right_rules_list(self):
        return self.rightOnly

    def get_union_list(self):
        return self.union




