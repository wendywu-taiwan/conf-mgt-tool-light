from RulesetComparer.dataModel.dataBuilder.ruleModifiedBuilder import RuleModifiedBuilder
from RulesetComparer.properties import dataKey as key


class RulesetComparer:
    def __init__(self, base_rule_set, compare_rule_set):
        self.base_rule_set = base_rule_set
        self.compare_rule_set = compare_rule_set
        self.baseKeyOnly = []
        self.compareKeyOnly = []
        self.different = []
        self.normal = []
        self.classify_rule_keys()

    def classify_rule_keys(self):
        base_key_set = set(self.base_rule_set.get_rules_name_list())
        compare_key_set = set(self.compare_rule_set.get_rules_name_list())

        # get rule key only in left rules
        self.baseKeyOnly = list(base_key_set - compare_key_set)
        self.baseKeyOnly.sort()
        # get rule key only in right rules
        self.compareKeyOnly = list(compare_key_set - base_key_set)
        self.compareKeyOnly.sort()

        # get union key in two rules
        tmp = list(base_key_set & compare_key_set)
        for rule_key in tmp:
            base_rule_value = self.base_rule_set.get_rule_full_value(rule_key)
            compare_rule_value = self.compare_rule_set.get_rule_full_value(rule_key)
            if base_rule_value != compare_rule_value:
                self.different.append(rule_key)
            else:
                self.normal.append(rule_key)
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
        for rule_key in self.different:
            # get xml rule model
            base_rule_model = self.base_rule_set.get_rule_by_key(rule_key)
            compare_rule_model = self.compare_rule_set.get_rule_by_key(rule_key)
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
