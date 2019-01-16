from RulesetComparer.dataModel.xml.baseParser import BaseModel
from RulesetComparer.dataModel.xml.ruleParser import RuleModel
from RulesetComparer.dataModel.dataBuilder.ruleSetBuilder import RuleSetBuilder
from RulesetComparer.properties import xmlKey as XMLKey


# this is for handling rules data, rules file contains many rules
class RulesModel(BaseModel):
    def __init__(self, xml, rule_name):
        BaseModel.__init__(self, xml)
        self.root = self.parse_xml_from_file()
        self.rulesName = rule_name
        self.rulesMap = {}
        self.parse_data()

    def parse_data(self):
        if not self.valid_data():
            return None

        self.check_xml_tag()

        # get data array in <Rule></Rule>
        if self.has_xml_tag:
            for rule in self.node_array_with_xml(self.root, XMLKey.NODE_KEY_RULE):
                rule_key = self.value_with_xml(rule, XMLKey.RULE_KEY)
                rule_model = RuleModel(rule, self.has_xml_tag)
                self.rulesMap[rule_key] = rule_model
        else:
            for rule in self.node_array(self.root, XMLKey.NODE_KEY_RULE):
                rule_key = self.value(rule, XMLKey.RULE_KEY)
                rule_model = RuleModel(rule, self.has_xml_tag)
                self.rulesMap[rule_key] = rule_model

    def get_rule_by_key(self, rule_key):
        return self.rulesMap[rule_key]

    def get_rules_name(self):
        return self.rulesName

    def get_rules_count(self):
        return len(self.rulesMap.keys())

    def get_rules_name_list(self):
        return list(self.rulesMap.keys())

    def get_rule_full_value(self, rule_key):
        rule = self.rulesMap[rule_key]

        if rule is None:
            return ""

        return rule.get_full_value()

    def get_rule_value(self, rule_key):
        rule = self.rulesMap[rule_key]

        if rule is None:
            return None
        return rule.get_rule_value()

    def get_rule_expression(self, rule_key):
        rule = self.rulesMap[rule_key]

        if rule is None:
            return None

        return rule.get_rule_expression()

    def get_rules_data_array(self, name_list=None):
        array = list()

        if name_list is None:
            name_list = self.get_rules_name_list()

        for rule in name_list:
            rule_model = self.rulesMap[rule]
            if rule_model is None:
                continue
            data_builder = RuleSetBuilder(rule_model)
            array.append(data_builder.get_data())
        return array
