from RulesetComparer.dataModel.dataBuilder.ruleModifiedBuilder import RuleModifiedBuilder
from RulesetComparer.dataModel.dataBuilder.rulesetCompareResultBuilder import RulesetCompareResultBuilder
from RulesetComparer.properties import dataKey as key
from RulesetComparer.utils.rulesetUtil import *


class RulesetComparer:
    LOG_CLASS = "RulesetComparer"

    def __init__(self, ruleset_name, base_ruleset, compare_ruleset, is_module):
        try:
            info_log(self.LOG_CLASS, '======== RulesetComparer compare %s ========' % ruleset_name)
            self.is_module = is_module
            self.ruleset_name = ruleset_name
            self.base_rule_set = None
            self.compare_rule_set = None
            self.baseKeyOnly = []
            self.compareKeyOnly = []
            self.different = []
            self.normal = []
            self.parse_ruleset(base_ruleset, compare_ruleset)
            self.classify_rule_keys()
            info_log(self.LOG_CLASS, '======== RulesetComparer compare finished ========')
        except Exception as e:
            raise e

    def parse_ruleset(self, base_ruleset, compare_ruleset):
        if self.is_module:
            self.base_rule_set = base_ruleset
            self.compare_rule_set = compare_ruleset
        else:
            self.base_rule_set = load_rule_module_from_file(self.ruleset_name, base_ruleset)
            self.compare_rule_set = load_rule_module_from_file(self.ruleset_name, compare_ruleset)

    def classify_rule_keys(self):
        base_key_set = set(self.base_rule_set.get_rule_combined_key_list())
        compare_key_set = set(self.compare_rule_set.get_rule_combined_key_list())

        # get rule key only in left rules
        self.baseKeyOnly = list(base_key_set - compare_key_set)
        self.baseKeyOnly.sort()
        # get rule key only in right rules
        self.compareKeyOnly = list(compare_key_set - base_key_set)
        self.compareKeyOnly.sort()

        # get union key in two rules
        tmp = list(base_key_set & compare_key_set)
        for combined_key in tmp:
            base_rule_value = self.base_rule_set.get_rule_full_value(combined_key)
            compare_rule_value = self.compare_rule_set.get_rule_full_value(combined_key)
            if base_rule_value != compare_rule_value:
                self.different.append(combined_key)
            else:
                self.normal.append(combined_key)
        self.different.sort()
        self.normal.sort()

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

    def get_base_rules_array(self):
        return self.base_rule_set.get_rules_data_array(self.baseKeyOnly)

    def get_compared_rules_array(self):
        return self.compare_rule_set.get_rules_data_array(self.compareKeyOnly)

    def get_difference_rules_array(self):
        data_array = list()
        for combined_key in self.different:
            # get xml rule model
            base_rule_model = self.base_rule_set.get_rule_by_key(combined_key)
            compare_rule_model = self.compare_rule_set.get_rule_by_key(combined_key)
            data_builder = RuleModifiedBuilder(base_rule_model, compare_rule_model)
            data_array.append(data_builder.get_data())

        return data_array

    def get_normal_rules_array(self):
        return self.base_rule_set.get_rules_data_array(self.normal)

    def get_diff_data(self):
        diff_result = {
            key.RULE_LIST_ITEM_TABLE_TYPE_ADD: self.get_compared_rules_array(),
            key.RULE_LIST_ITEM_TABLE_TYPE_REMOVE: self.get_base_rules_array(),
            key.RULE_LIST_ITEM_TABLE_TYPE_MODIFY: self.get_difference_rules_array(),
            key.RULE_LIST_ITEM_TABLE_TYPE_NORMAL: self.get_normal_rules_array()
        }
        return diff_result

    def get_data_by_builder(self):
        builder = RulesetCompareResultBuilder(self.base_rule_set.get_rules_name(),
                                              self.get_base_rules_array(),
                                              self.get_compared_rules_array(),
                                              self.get_difference_rules_array(),
                                              self.get_normal_rules_array())

        return builder.get_data()
