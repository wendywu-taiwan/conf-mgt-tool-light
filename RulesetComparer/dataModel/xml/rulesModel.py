from RulesetComparer.dataModel.xml.baseModel import BaseModel
from RulesetComparer.properties import xmlKey as XMLKey
from RulesetComparer.dataModel.xml.ruleModel import RuleModel


# this is for handling rules data, rules file contains many rules
class RulesModel(BaseModel):
    def __init__(self, xml):
        BaseModel.__init__(self, xml)
        self.root = self.parse_xml_from_file()
        self.rulesName = ""
        self.rulesMap = {}
        self.parse_data()

    def parse_data(self):
        if not self.valid_data():
            return None
        # get data array in <Rule></Rule>
        for rule in self.node_array(self.root, XMLKey.NODE_KEY_RULE):
            self.rulesName = self.value_in_node(rule,
                                                XMLKey.NODE_KEY_CONTEXT,
                                                XMLKey.ORGANIZATION_ID)
            # get data array in <Key></Key>
            rule_key = self.value(rule, XMLKey.RULE_KEY)
            rule_model = RuleModel(rule)
            self.rulesMap[rule_key] = rule_model

    def get_rules_name(self):
        return self.rulesName

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
        value = rule.get_rule_value().split(' ', 1 )
        return rule.get_rule_value()

    def get_rule_expression(self, rule_key):
        rule = self.rulesMap[rule_key]

        if rule is None:
            return None

        return rule.get_rule_expression()

    def get_rules_map(self):
        return self.rulesMap

    def get_rules_data_array(self, name_list=None):
        array = list()

        if name_list is None:
            name_list = self.get_rules_name_list()

        for rule in name_list:
            rule_model = self.rulesMap[rule]
            if rule_model is None:
                continue
            array.append(rule_model.generate_result_dict())
        return array


