import RulesetComparer.properties.parserKey as parser


class RuleListItemModel:

    def __init__(self, rule_module, base_env_id, compare_env_id, compare_hash_key):
        self.rule_module = rule_module
        self.data_to_serialize = {
            parser.RULE_LIST_ITEM_NAME: rule_module.get_rules_name(),
            parser.RULE_LIST_ITEM_BASE_ENV_ID: base_env_id,
            parser.RULE_LIST_ITEM_COMPARE_ENV_ID: compare_env_id,
            parser.RULE_LIST_ITEM_COMPARE_HASH_KEY: compare_hash_key,
            parser.RULE_LIST_ITEM_BASE_COUNT: 0,
            parser.RULE_LIST_ITEM_NEW_COUNT: 0,
            parser.RULE_LIST_ITEM_ADD_COUNT: 0,
            parser.RULE_LIST_ITEM_MINUS_COUNT: 0,
            parser.RULE_LIST_ITEM_MODIFY_COUNT: 0
        }

    def set_normal_rule(self):
        self.data_to_serialize[parser.RULE_LIST_ITEM_BASE_COUNT] = self.rule_module.get_rules_count()
        self.data_to_serialize[parser.RULE_LIST_ITEM_NEW_COUNT] = self.rule_module.get_rules_count()

    def set_add_rule(self):
        self.data_to_serialize[parser.RULE_LIST_ITEM_NEW_COUNT] = self.rule_module.get_rules_count()
        self.data_to_serialize[parser.RULE_LIST_ITEM_ADD_COUNT] = self.rule_module.get_rules_count()

    def set_minus_rule(self):
        self.data_to_serialize[parser.RULE_LIST_ITEM_BASE_COUNT] = self.rule_module.get_rules_count()
        self.data_to_serialize[parser.RULE_LIST_ITEM_MINUS_COUNT] = self.rule_module.get_rules_count()

    def set_modify_rule(self, base_count, new_count, add_count, minus_count, modify_count):
        self.data_to_serialize[parser.RULE_LIST_ITEM_BASE_COUNT] = base_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_NEW_COUNT] = new_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_ADD_COUNT] = add_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_MINUS_COUNT] = minus_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_MODIFY_COUNT] = modify_count

    def get_data(self):
        return self.data_to_serialize
