from RulesetComparer.dataModel.xml.baseParser import BaseModel
from RulesetComparer.properties import xmlKey as XMLKey
from RulesetComparer.utils import logger
from lxml import etree


# this is for handling single rule in a ruleset file
class RuleModel(BaseModel):
    def __init__(self, xml, has_saxif_tag):
        BaseModel.__init__(self, xml)
        self.has_saxif_tag = has_saxif_tag
        self.countryOrganizationId = None
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
        self.countryOrganizationId = self.node_value(key=XMLKey.COUNTRY_ORGANIZATION_ID)
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

    def to_xml(self):
        rule = etree.Element(XMLKey.NODE_KEY_RULE)

        etree.SubElement(rule, XMLKey.COUNTRY_ORGANIZATION_ID).text = self.countryOrganizationId

        context = etree.SubElement(rule, XMLKey.NODE_KEY_CONTEXT)
        if self.process != '':
            etree.SubElement(context, XMLKey.PROCESS).text = self.process
        if self.processStep != '':
            etree.SubElement(context, XMLKey.PROCESS_STEP).text = self.processStep
        if self.ownerRole != '':
            etree.SubElement(context, XMLKey.OWNER_RULE).text = self.ownerRole

        etree.SubElement(context, XMLKey.ORGANIZATION_ID).text = self.organizationId
        etree.SubElement(rule, XMLKey.RULE_TYPE).text = self.ruleType
        etree.SubElement(rule, XMLKey.RULE_KEY).text = self.ruleKey
        etree.SubElement(rule, XMLKey.RULE_VALUE).text = self.ruleValue
        if self.expression != '':
            etree.SubElement(rule, XMLKey.EXPRESSION).text = self.expression
        etree.SubElement(rule, XMLKey.STATUS).text = 'Active'
        etree.SubElement(rule, XMLKey.CREATED_BY).text = 'mid_Member.Manager'
        etree.SubElement(rule, XMLKey.LAST_UPDATE_DBY).text = 'mid_Member.Manager'

        # logger.info_log("RuleModel", etree.tostring(rule, pretty_print=True))
        return rule

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
