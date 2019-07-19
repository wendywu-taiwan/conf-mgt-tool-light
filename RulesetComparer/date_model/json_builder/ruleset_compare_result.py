from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties import dataKey as key


class RulesetCompareResultBuilder(BaseBuilder):
    def __init__(self, ruleset_name, source_env_only_rules, target_env_only_rules, different_rules, normal_rules):
        self.ruleset_name = ruleset_name
        self.source_env_only_rules = source_env_only_rules
        self.target_env_only_rules = target_env_only_rules
        self.different_rules = different_rules
        self.normal_rules = normal_rules
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict["name"] = self.ruleset_name
        self.result_dict["source_env_only_rules"] = self.__generate_rules_obj__(
            len(self.source_env_only_rules), self.source_env_only_rules)
        self.result_dict["target_env_only_rules"] = self.__generate_rules_obj__(
            len(self.target_env_only_rules), self.target_env_only_rules)
        self.result_dict["normal_rules"] = self.__generate_rules_obj__(
            len(self.normal_rules), self.normal_rules)
        self.result_dict["different_rules"] = self.__generate_rules_obj__(
            len(self.different_rules), self.different_rules)

    @staticmethod
    def __generate_rules_obj__(ruleset_type_count, ruleset_diff_type_list):
        rules_obj = {}
        rules_array = []
        for rule_detail in ruleset_diff_type_list:
            rule_obj = {"combined_key": rule_detail[key.RULE_KEY_COMBINED_KEY]}
            rules_array.append(rule_obj)

        rules_obj["count"] = ruleset_type_count
        rules_obj["rules_array"] = rules_array
        return rules_obj
