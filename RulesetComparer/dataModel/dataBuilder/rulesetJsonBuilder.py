from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.dataKey import *


class RulesetJsonBuilder(BaseBuilder):
    def __init__(self, ruleset_data=None):
        self.ruleset_data = ruleset_data
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[RULE_KEY_COMBINED_KEY] = self.ruleset_data.get(RULE_KEY_COMBINED_KEY)
        self.result_dict[RULE_KEY_PROCESS] = self.ruleset_data.get(RULE_KEY_PROCESS)
        self.result_dict[RULE_KEY_PROCESS_STEP] = self.ruleset_data.get(RULE_KEY_PROCESS_STEP)
        self.result_dict[RULE_KEY_ORGANIZATION_ID] = self.ruleset_data.get(RULE_KEY_ORGANIZATION_ID)
        self.result_dict[RULE_KEY_OWNER_RULE] = self.ruleset_data.get(RULE_KEY_OWNER_RULE)
        self.result_dict[RULE_KEY_RULE_TYPE] = self.ruleset_data.get(RULE_KEY_RULE_TYPE)
        self.result_dict[RULE_KEY_RULE_KEY] = self.ruleset_data.get(RULE_KEY_RULE_KEY)
        self.result_dict[RULE_KEY_RULE_VALUE] = self.ruleset_data.get(RULE_KEY_RULE_VALUE)
        self.result_dict[RULE_KEY_RULE_EXPRESSION] = self.ruleset_data.get(RULE_KEY_RULE_EXPRESSION)

