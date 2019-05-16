

class RuleListComparer:
    def __init__(self, base_env_rulesets, compare_env_rulesets):
        self.base_env_rulesets = base_env_rulesets
        self.compare_env_rulesets = compare_env_rulesets
        self.baseEnvOnly = []
        self.comparedEnvOnly = []
        self.union = []
        self.classify_rule_list()

    def classify_rule_list(self):
        base_env_key_set = set(self.base_env_rulesets)
        compared_env_key_set = set(self.compare_env_rulesets)

        # get rule key only in left rules
        self.baseEnvOnly = list(base_env_key_set - compared_env_key_set)
        self.baseEnvOnly.sort()
        # get rule key only in right rules
        self.comparedEnvOnly = list(compared_env_key_set - base_env_key_set)
        self.comparedEnvOnly.sort()
        # get union key in two rules
        self.union = list(base_env_key_set & compared_env_key_set)
        self.union.sort()

    def get_base_rules_list(self):
        return self.baseEnvOnly

    def get_compare_rules_list(self):
        return self.comparedEnvOnly

    def get_union_list(self):
        return self.union




