from RulesetComparer.dataModel.xml.baseParser import BaseModel
from RulesetComparer.properties import xmlKey as XMLKey


# this is for handling single rule in a ruleset file
class RuleModel(BaseModel):
    def __init__(self, xml, has_saxif_tag):
        BaseModel.__init__(self, xml)
        self.has_saxif_tag = has_saxif_tag
        self.combinedKey = None
        self.fullValue = None
        self.process = None
        self.processStep = None
        self.organizationId = None
        self.ownerRole = None
        self.ruleType = None
        self.ruleKey = None
        self.ruleValue = None
        self.expression = None
        self.parse_data_catch_error()

    def parse_data(self):
        self.process = self.value_in_context(key=XMLKey.PROCESS)
        self.processStep = self.value_in_context(key=XMLKey.PROCESS_STEP)
        self.organizationId = self.value_in_context(key=XMLKey.ORGANIZATION_ID)
        self.ownerRole = self.value_in_context(key=XMLKey.OWNER_RULE)
        self.ruleType = self.node_value(key=XMLKey.RULE_TYPE)
        self.ruleKey = self.node_value(key=XMLKey.RULE_KEY)
        self.ruleValue = self.node_value(key=XMLKey.RULE_VALUE)
        self.expression = self.node_value(key=XMLKey.EXPRESSION)

        self.combinedKey = self._gen_combined_key()
        self.fullValue = self._full_value()

    def _gen_combined_key(self):
        return '\t'.join([self.process, self.processStep, self.ownerRole, self.ruleType, self.ruleKey])

    def _full_value(self):
        return '\t'.join([self.ruleValue, self.expression])

    def node_value(self, key):
        return self.node_value_data(self.xml, saxif_tag=self.has_saxif_tag, node_key=key, node_path=key)

    def value_in_context(self, key):
        nest_path = XMLKey.NODE_KEY_CONTEXT + "/" + key
        return self.nest_node_value_data(data=self.xml,
                                         saxif_tag=self.has_saxif_tag,
                                         node_key=XMLKey.NODE_KEY_CONTEXT,
                                         value_key=key,
                                         node_path=nest_path)
