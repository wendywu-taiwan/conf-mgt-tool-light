

class RuleListComparer:
    def __init__(self, base_rule_list, compare_rule_list):
        self.base_rule_list = base_rule_list
        self.compare_rule_list = compare_rule_list
        self.baseOnly = []
        self.comparedOnly = []
        self.union = []
        self.classify_rule_list()

    def classify_rule_list(self):
        base_key_set = set(self.base_rule_list)
        compared_key_set = set(self.compare_rule_list)

        # get rule key only in left rules
        self.baseOnly = list(base_key_set - compared_key_set)
        # get rule key only in right rules
        self.comparedOnly = list(compared_key_set - base_key_set)

        # get union key in two rules
        self.union = list(base_key_set & compared_key_set)

    def get_base_rules_list(self):
        return self.baseOnly

    def get_compare_rules_list(self):
        return self.comparedOnly

    def get_union_list(self):
        return self.union




