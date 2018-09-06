from RulesetComparer.dataModel.xml.baseModel import BaseModel
from RulesetComparer.resource import xmlKey as XMLKey


class RulesetModel(BaseModel):
    def __init__(self, xml):
        BaseModel.__init__(self, xml)
        self.rule_module_map = {}
        self.parse_xml_from_file()

    def parse_data(self):
        if not self.valid_rule_set():
            return None

        # get data array in <Rule></Rule>
        for rule_data in self.get_node_array(self.root, XMLKey.XML_KEY_RULE):
            # get data array in <Key></Key>
            rule_key = self.get_value(rule_data, XMLKey.XML_KEY_RULE_KEY)
            self.rule_module_map[rule_key] = [rule_data]

    def valid_rule(self, rule_key):
        if rule_key is None or rule_key not in self.rule_module_map:
            return False
        rule = self.rule_module_map[rule_key]
        if len(rule) != XMLKey.XML_NODE_COUNT:
            return False
        return True

    def get_ruleset_key_list(self):
        return list(self.rule_module_map.keys())

    def contains_ruleset(self, rule_key):
        return rule_key in self.rule_module_map
