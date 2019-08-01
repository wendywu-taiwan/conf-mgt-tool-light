from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.serializers.serializers import ModifiedRuleValueSerializer
from RulesetComparer.properties.key import *
from RulesetComparer.date_model.json_builder.ruleset_json import RulesetJsonBuilder


class DiffRulesetPageBuilder(BaseBuilder):
    def __init__(self, ruleset_name, source_env_name, target_env_name, compare_result_json):
        try:
            self.ruleset_name = ruleset_name
            self.source_env_name = source_env_name
            self.target_env_name = target_env_name
            self.data = compare_result_json
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        add_list = self.data[RULE_LIST_ITEM_TABLE_TYPE_ADD]
        remove_list = self.data[RULE_LIST_ITEM_TABLE_TYPE_REMOVE]
        modify_list = self.data[RULE_LIST_ITEM_TABLE_TYPE_MODIFY]
        normal_list = self.data[RULE_LIST_ITEM_TABLE_TYPE_NORMAL]

        self.result_dict[RULE_KEY_RULE_NAME] = self.ruleset_name
        self.result_dict[RULE_DIFF_KEY_BASE_ENV_NAME] = self.source_env_name
        self.result_dict[RULE_DIFF_KEY_COMPARED_ENV_NAME] = self.target_env_name
        self.result_dict[RULE_DIFF_KEY_ADD_LIST] = add_list
        self.result_dict[RULE_DIFF_KEY_REMOVE_LIST] = remove_list
        self.result_dict[RULE_DIFF_KEY_MODIFY_LIST] = modify_list
        self.result_dict[RULE_DIFF_KEY_NORMAL_LIST] = normal_list

        if len(add_list) == 0 and len(remove_list) == 0 and len(modify_list) == 0:
            self.result_dict[RULE_DIFF_HAS_CHANGES] = False
        else:
            self.result_dict[RULE_DIFF_HAS_CHANGES] = True