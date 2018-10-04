from RulesetComparer.dataModel.xml.baseParser import BaseModel
from RulesetComparer.properties import xmlKey as XMLKey


# this is for handling rule data
class RuleModel(BaseModel):
    def __init__(self, xml, has_xml_tag):
        BaseModel.__init__(self, xml)
        if has_xml_tag:
            self.__init_with_xml_tag(xml)
        else:
            self.__init_no_xml_tag(xml)

    def __init_with_xml_tag(self, xml):
        self.process = self.value_in_context_with_xml(XMLKey.PROCESS)
        self.processStep = self.value_in_context_with_xml(XMLKey.PROCESS_STEP)
        self.organizationId = self.value_in_context_with_xml(XMLKey.ORGANIZATION_ID)
        self.ownerRole = self.value_in_context_with_xml(XMLKey.OWNER_RULE)
        self.ruleType = self.value_with_xml(xml, XMLKey.RULE_TYPE)
        self.ruleKey = self.value_with_xml(xml, XMLKey.RULE_KEY)
        self.ruleValue = self.value_with_xml(xml, XMLKey.RULE_VALUE)
        self.expression = self.value_with_xml(xml, XMLKey.EXPRESSION)
        self.fullValue = self.full_value()

    def __init_no_xml_tag(self, xml):
        self.process = self.value_in_context(XMLKey.PROCESS)
        self.processStep = self.value_in_context(XMLKey.PROCESS_STEP)
        self.organizationId = self.value_in_context(XMLKey.ORGANIZATION_ID)
        self.ownerRole = self.value_in_context(XMLKey.OWNER_RULE)
        self.ruleType = self.value(xml, XMLKey.RULE_TYPE)
        self.ruleKey = self.value(xml, XMLKey.RULE_KEY)
        self.ruleValue = self.value(xml, XMLKey.RULE_VALUE)
        self.expression = self.value(xml, XMLKey.EXPRESSION)
        self.fullValue = self.full_value()

    def parse_data(self):
        pass

    def get_rule_value(self):
        return self.ruleValue

    def get_rule_expression(self):
        return self.expression

    def get_full_value(self):
        return self.fullValue

    def full_value(self):
        return '\t'.join([self.ruleValue, self.expression])

    def valid_data(self):
        if self.xml is None or len(self.xml) != XMLKey.XML_NODE_COUNT:
            return False
        else:
            return True

    def value_in_context_with_xml(self, key):
        return self.value_in_node_with_xml(self.xml, XMLKey.NODE_KEY_CONTEXT, key)

    def value_in_context(self, key):
        return self.value(self.xml, XMLKey.NODE_KEY_CONTEXT + "/" + key)
