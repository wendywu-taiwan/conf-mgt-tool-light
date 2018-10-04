import RulesetComparer.properties.dataKey as key
from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder


class RuleListItemBuilder(BaseBuilder):

    def __init__(self, rule_module, compare_hash_key):
        self.rule_module = rule_module
        self.compare_hash_key = compare_hash_key
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict = {
            key.RULE_LIST_ITEM_NAME: self.rule_module.get_rules_name(),
            key.RULE_LIST_ITEM_COMPARE_HASH_KEY: self.compare_hash_key,
            key.RULE_LIST_ITEM_BASE_COUNT: 0,
            key.RULE_LIST_ITEM_NEW_COUNT: 0,
            key.RULE_LIST_ITEM_ADD_COUNT: 0,
            key.RULE_LIST_ITEM_REMOVE_COUNT: 0,
            key.RULE_LIST_ITEM_MODIFY_COUNT: 0
        }

    def set_normal_rule(self):
        self.result_dict[key.RULE_LIST_ITEM_TABLE_TYPE] = key.RULE_LIST_ITEM_TABLE_TYPE_NORMAL
        self.result_dict[key.RULE_LIST_ITEM_BASE_COUNT] = self.rule_module.get_rules_count()
        self.result_dict[key.RULE_LIST_ITEM_NEW_COUNT] = self.rule_module.get_rules_count()

    def set_add_rule(self):
        self.result_dict[key.RULE_LIST_ITEM_COMPARED_ENV_DATA] = self.rule_module.get_rules_data_array()
        self.result_dict[key.RULE_LIST_ITEM_TABLE_TYPE] = key.RULE_LIST_ITEM_TABLE_TYPE_ADD
        self.result_dict[key.RULE_LIST_ITEM_NEW_COUNT] = self.rule_module.get_rules_count()
        self.result_dict[key.RULE_LIST_ITEM_ADD_COUNT] = self.rule_module.get_rules_count()

    def set_remove_rule(self):
        self.result_dict[key.RULE_LIST_ITEM_BASE_ENV_DATA] = self.rule_module.get_rules_data_array()
        self.result_dict[key.RULE_LIST_ITEM_TABLE_TYPE] = key.RULE_LIST_ITEM_TABLE_TYPE_REMOVE
        self.result_dict[key.RULE_LIST_ITEM_BASE_COUNT] = self.rule_module.get_rules_count()
        self.result_dict[key.RULE_LIST_ITEM_REMOVE_COUNT] = self.rule_module.get_rules_count()

    def set_modify_rule(self, base_count, new_count, add_count, remove_count, modify_count):
        self.result_dict[key.RULE_LIST_ITEM_TABLE_TYPE] = key.RULE_LIST_ITEM_TABLE_TYPE_MODIFY
        self.result_dict[key.RULE_LIST_ITEM_BASE_COUNT] = base_count
        self.result_dict[key.RULE_LIST_ITEM_NEW_COUNT] = new_count
        self.result_dict[key.RULE_LIST_ITEM_ADD_COUNT] = add_count
        self.result_dict[key.RULE_LIST_ITEM_REMOVE_COUNT] = remove_count
        self.result_dict[key.RULE_LIST_ITEM_MODIFY_COUNT] = modify_count
