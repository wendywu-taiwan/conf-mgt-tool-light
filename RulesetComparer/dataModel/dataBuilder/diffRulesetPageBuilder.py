from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.serializers.serializers import RuleSerializer, ModifiedRuleValueSerializer
from RulesetComparer.properties.dataKey import *


class DiffRulesetPageBuilder(BaseBuilder):
    def __init__(self, ruleset_name, base_env_name, compared_env_name, compare_result_json):
        try:
            self.ruleset_name = ruleset_name
            self.base_env_name = base_env_name
            self.compared_env_name = compared_env_name
            self.data = compare_result_json
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        add_list = RuleSerializer(self.data[RULE_LIST_ITEM_TABLE_TYPE_ADD], many=True).data
        remove_list = RuleSerializer(self.data[RULE_LIST_ITEM_TABLE_TYPE_REMOVE], many=True).data
        modify_list = ModifiedRuleValueSerializer(self.data[RULE_LIST_ITEM_TABLE_TYPE_MODIFY], many=True).data
        normal_list = RuleSerializer(self.data[RULE_LIST_ITEM_TABLE_TYPE_NORMAL], many=True).data

        self.result_dict[RULE_KEY_RULE_NAME] = self.ruleset_name
        self.result_dict[RULE_DIFF_KEY_BASE_ENV_NAME] = self.base_env_name
        self.result_dict[RULE_DIFF_KEY_COMPARED_ENV_NAME] = self.compared_env_name
        self.result_dict[RULE_DIFF_KEY_ADD_LIST] = add_list
        self.result_dict[RULE_DIFF_KEY_REMOVE_LIST] = remove_list
        self.result_dict[RULE_DIFF_KEY_MODIFY_LIST] = modify_list
        self.result_dict[RULE_DIFF_KEY_NORMAL_LIST] = normal_list

        if len(add_list) == 0 and len(remove_list) == 0 and len(modify_list) == 0:
            self.result_dict[RULE_DIFF_HAS_CHANGES] = False
        else:
            self.result_dict[RULE_DIFF_HAS_CHANGES] = True
