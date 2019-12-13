from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties import key as key


class RuleModifiedBuilder(BaseBuilder):
    def __init__(self, base_model, compare_model, source_value_data, target_value_data, source_expression_data,
                 target_expression_data):
        self.base_model = base_model
        self.compare_model = compare_model
        self.source_value_data = source_value_data
        self.target_value_data = target_value_data
        self.source_expression_data = source_expression_data
        self.target_expression_data = target_expression_data
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[key.RULE_KEY_COMBINED_KEY] = self.base_model.combinedKey
        self.result_dict[key.RULE_KEY_PROCESS] = self.base_model.process
        self.result_dict[key.RULE_KEY_PROCESS_STEP] = self.base_model.processStep
        self.result_dict[key.RULE_KEY_ORGANIZATION_ID] = self.base_model.organizationId
        self.result_dict[key.RULE_KEY_OWNER_RULE] = self.base_model.ownerRole
        self.result_dict[key.RULE_KEY_RULE_TYPE] = self.base_model.ruleType
        self.result_dict[key.RULE_KEY_RULE_KEY] = self.base_model.ruleKey
        self.result_dict[key.RULE_MODIFIED_KEY_BASE_VALUE] = self.source_value_data
        self.result_dict[key.RULE_MODIFIED_KEY_BASE_EXPRESSION] = self.source_expression_data
        self.result_dict[key.RULE_MODIFIED_KEY_COMPARE_VALUE] = self.target_value_data
        self.result_dict[key.RULE_MODIFIED_KEY_COMPARE_EXPRESSION] = self.target_expression_data
