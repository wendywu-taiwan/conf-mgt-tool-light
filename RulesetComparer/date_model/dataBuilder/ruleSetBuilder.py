from RulesetComparer.date_model.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties import dataKey as key


class RuleSetBuilder(BaseBuilder):
    def __init__(self, rule_model):
        self.rule_model = rule_model
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[key.RULE_KEY_COMBINED_KEY] = self.rule_model.combinedKey
        self.result_dict[key.RULE_KEY_PROCESS] = self.rule_model.process
        self.result_dict[key.RULE_KEY_PROCESS_STEP] = self.rule_model.processStep
        self.result_dict[key.RULE_KEY_ORGANIZATION_ID] = self.rule_model.organizationId
        self.result_dict[key.RULE_KEY_OWNER_RULE] = self.rule_model.ownerRole
        self.result_dict[key.RULE_KEY_RULE_TYPE] = self.rule_model.ruleType
        self.result_dict[key.RULE_KEY_RULE_KEY] = self.rule_model.ruleKey
        self.result_dict[key.RULE_KEY_RULE_VALUE] = self.split_data(self.rule_model.ruleValue)
        self.result_dict[key.RULE_KEY_RULE_EXPRESSION] = self.split_data(self.rule_model.expression)

    @staticmethod
    def split_data(data):
        return data.split(",")
