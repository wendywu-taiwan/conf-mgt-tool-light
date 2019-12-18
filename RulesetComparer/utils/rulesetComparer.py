from RulesetComparer.date_model.json_builder.ruleset_json import RulesetJsonBuilder
from RulesetComparer.date_model.json_builder.ruleset_modified import RuleModifiedBuilder
from RulesetComparer.date_model.json_builder.ruleset_compare_result import RulesetCompareResultBuilder
from RulesetComparer.properties import key as key
from RulesetComparer.serializers.serializers import ModifiedRuleValueSerializer
from RulesetComparer.utils.rulesetUtil import *
from common.data_object.string_diff_object import StringDiffObject


class RulesetComparer:
    LOG_CLASS = "RulesetComparer"

    def __init__(self, ruleset_name, source_ruleset, target_ruleset, is_module):
        try:
            info_log(self.LOG_CLASS, '======== RulesetComparer compare %s ========' % ruleset_name)
            self.is_module = is_module
            self.ruleset_name = ruleset_name
            self.source_ruleset = None
            self.target_ruleset = None
            self.sourceKeyOnly = []
            self.targetKeyOnly = []
            self.different = []
            self.normal = []
            self.source_different_value_rules_map = {}
            self.target_different_value_rules_map = {}
            self.source_different_expression_rules_map = {}
            self.target_different_expression_rules_map = {}
            self.parse_ruleset(source_ruleset, target_ruleset)
            self.classify_rule_keys()
            info_log(self.LOG_CLASS, '======== RulesetComparer compare finished ========')
        except Exception as e:
            raise e

    def parse_ruleset(self, source_ruleset, target_ruleset):
        if self.is_module:
            self.source_ruleset = source_ruleset
            self.target_ruleset = target_ruleset
        else:
            self.source_ruleset = load_rule_module_from_file(self.ruleset_name, source_ruleset)
            self.target_ruleset = load_rule_module_from_file(self.ruleset_name, target_ruleset)

    def classify_rule_keys(self):
        source_key_set = set(self.source_ruleset.get_rule_combined_key_list())
        target_key_set = set(self.target_ruleset.get_rule_combined_key_list())

        # get rule key only in left rules
        self.sourceKeyOnly = list(source_key_set - target_key_set)
        self.sourceKeyOnly.sort()
        # get rule key only in right rules
        self.targetKeyOnly = list(target_key_set - source_key_set)
        self.targetKeyOnly.sort()

        same_key = list(source_key_set & target_key_set)

        # get union key in two rules
        for combined_key in same_key:
            source_full_value = self.source_ruleset.get_rule_full_value(combined_key)
            target_full_value = self.target_ruleset.get_rule_full_value(combined_key)
            if source_full_value == target_full_value:
                self.normal.append(combined_key)
            else:
                # generate rules value diff result
                source_value = self.source_ruleset.get_rule_value(combined_key)
                target_value = self.target_ruleset.get_rule_value(combined_key)
                self.diff_value_expression(combined_key, source_value, target_value,
                                           self.source_different_value_rules_map,
                                           self.target_different_value_rules_map)

                # generate rules expression diff result
                source_expression = self.source_ruleset.get_rule_expression(combined_key)
                target_expression = self.target_ruleset.get_rule_expression(combined_key)
                self.diff_value_expression(combined_key, source_expression, target_expression,
                                           self.source_different_expression_rules_map,
                                           self.target_different_expression_rules_map)
                self.different.append(combined_key)
        self.different.sort()
        self.normal.sort()

    @staticmethod
    def diff_value_expression(combined_key, source_data, target_data, source_map, target_map):
        diff_object = StringDiffObject([source_data, target_data])
        diff_object.diff()
        source_map[combined_key] = diff_object.get_left_data()
        target_map[combined_key] = diff_object.get_right_data()

    def no_difference(self):
        if len(self.sourceKeyOnly) == 0 and len(self.targetKeyOnly) == 0 and len(self.different) == 0:
            return True
        return False

    def get_source_only_count(self):
        return len(self.sourceKeyOnly)

    def get_target_only_count(self):
        return len(self.targetKeyOnly)

    def get_difference_count(self):
        return len(self.different)

    def get_diff_data(self):
        diff_result = {
            key.RULE_LIST_ITEM_TABLE_TYPE_ADD: self.parse_list_data(self.get_target_rules_array()),
            key.RULE_LIST_ITEM_TABLE_TYPE_REMOVE: self.parse_list_data(self.get_source_rules_array()),
            key.RULE_LIST_ITEM_TABLE_TYPE_MODIFY: self.get_difference_rules_array(),
            key.RULE_LIST_ITEM_TABLE_TYPE_NORMAL: self.parse_list_data(self.get_normal_rules_array())
        }
        return diff_result

    @staticmethod
    def parse_list_data(rulesets_data):
        data_list = []
        for ruleset_data in rulesets_data:
            data = RulesetJsonBuilder(ruleset_data).get_data()
            data_list.append(data)
        return data_list

    def get_data_by_builder(self):
        builder = RulesetCompareResultBuilder(self.source_ruleset.get_rules_name(),
                                              self.get_source_rules_array(),
                                              self.get_target_rules_array(),
                                              self.get_difference_rules_array(),
                                              self.get_normal_rules_array())

        return builder.get_data()

    def get_source_rules_array(self):
        return self.source_ruleset.get_rules_data_array(self.sourceKeyOnly)

    def get_target_rules_array(self):
        return self.target_ruleset.get_rules_data_array(self.targetKeyOnly)

    def get_difference_rules_array(self):
        data_array = list()
        for combined_key in self.different:
            # get xml rule model
            base_rule_model = self.source_ruleset.get_rule_by_key(combined_key)
            compare_rule_model = self.target_ruleset.get_rule_by_key(combined_key)
            s_value_diff_result = self.source_different_value_rules_map[combined_key]
            s_expression_diff_result = self.source_different_expression_rules_map[combined_key]
            t_value_diff_result = self.target_different_value_rules_map[combined_key]
            t_expression_diff_result = self.target_different_expression_rules_map[combined_key]

            data_builder = RuleModifiedBuilder(base_rule_model, compare_rule_model,
                                               s_value_diff_result, t_value_diff_result,
                                               s_expression_diff_result, t_expression_diff_result)
            data_array.append(data_builder.get_data())

        return data_array

    def get_normal_rules_array(self):
        return self.source_ruleset.get_rules_data_array(self.normal)
