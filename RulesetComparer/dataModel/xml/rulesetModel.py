import xml.etree.ElementTree as ET
from RulesetComparer.resource import xmlKey as XMLKey


class RulesetModel:
    def __init__(self, rules):
        xml_tree = ET.parse(rules)
        self.rules = rules
        self.root = xml_tree.getroot()
        self.rule_module_map = {}
        self.parse_rule_model()

    def parse_rule_model(self):
        if not self.valid_rule_set():
            return None

        for rule_data in self.root.findall(XMLKey.filter_with_key(XMLKey.XML_KEY_RULE),
                                           XMLKey.XML_PATH_MAP):

            rule_key = self.get_value(rule_data, XMLKey.XML_KEY_RULE_KEY)
            self.rule_module_map[rule_key] = [rule_data]
            print("rule_key = %s ,  rule_data = %s" % (rule_key, rule_data ))

    def get_node_value(self, rule_key, value_key):
        rule_data = self.rule_module_map[rule_key]
        return self.get_value(rule_data, value_key)

    @staticmethod
    def get_value(data, key):
        if data is None:
            return None

        value = data.find(XMLKey.filter_with_key(key), XMLKey.XML_PATH_MAP).text
        return value

    def valid_rule_set(self):
        if self.root is None:
            return False
        else:
            return True

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
