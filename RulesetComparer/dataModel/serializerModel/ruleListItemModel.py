import RulesetComparer.properties.parserKey as parser


class RuleListItemModel:

    def __init__(self):
        self.data_to_serialize = {
            parser.RULE_LIST_ITEM_NAME: "",
            parser.RULE_LIST_ITEM_BASE_COUNT: 0,
            parser.RULE_LIST_ITEM_NEW_COUNT: 0,
            parser.RULE_LIST_ITEM_ADD_COUNT: 0,
            parser.RULE_LIST_ITEM_MINUS_COUNT: 0,
            parser.RULE_LIST_ITEM_MODIFY_COUNT: 0
        }

    def set_normal_rule(self, rule_module):
        self.data_to_serialize[parser.RULE_LIST_ITEM_NAME] = rule_module.get_rules_name()
        self.data_to_serialize[parser.RULE_LIST_ITEM_BASE_COUNT] = rule_module.get_rules_count()
        self.data_to_serialize[parser.RULE_LIST_ITEM_NEW_COUNT] = rule_module.get_rules_count()

    def set_add_rule(self, rule_module):
        self.data_to_serialize[parser.RULE_LIST_ITEM_NAME] = rule_module.get_rules_name()
        self.data_to_serialize[parser.RULE_LIST_ITEM_NEW_COUNT] = rule_module.get_rules_count()
        self.data_to_serialize[parser.RULE_LIST_ITEM_ADD_COUNT] = rule_module.get_rules_count()

    def set_minus_rule(self, rule_module):
        self.data_to_serialize[parser.RULE_LIST_ITEM_NAME] = rule_module.get_rules_name()
        self.data_to_serialize[parser.RULE_LIST_ITEM_BASE_COUNT] = rule_module.get_rules_count()
        self.data_to_serialize[parser.RULE_LIST_ITEM_MINUS_COUNT] = rule_module.get_rules_count()

    def set_modify_rule(self,rule_name, base_count, new_count, add_count, minus_count, modify_count):
        self.data_to_serialize[parser.RULE_LIST_ITEM_NAME] = rule_name
        self.data_to_serialize[parser.RULE_LIST_ITEM_BASE_COUNT] = base_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_NEW_COUNT] = new_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_ADD_COUNT] = add_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_MINUS_COUNT] = minus_count
        self.data_to_serialize[parser.RULE_LIST_ITEM_MODIFY_COUNT] = modify_count

    def get_data(self):
        return self.data_to_serialize
