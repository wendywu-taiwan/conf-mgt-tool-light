import xml.etree.ElementTree as ET
from RulesetComparer.resource import xmlKey as XMLKey


class RuleListModel:
    def __init__(self, xml):
        # xml_tree = ET.fromstring(xml)
        self.xml = xml
        self.root = ET.fromstring(xml)
        self.rule_key_list = []
        self.parse_data()

    def parse_data(self):
        if not self.valid_data():
            return

        for rule_data in self.root.findall(XMLKey.filter_with_key(XMLKey.XML_KEY_RULE),
                                           XMLKey.XML_PATH_MAP):
            print(rule_data.tag, rule_data.attrib, rule_data.text)
            context = self.get_node(rule_data, XMLKey.XML_KEY_CONTEXT)
            rule_key = self.get_value(context, XMLKey.XML_KEY_ORGANIZATIONID)
            print(rule_key)

        #     rule_key = self.get_value(context_data, XMLKey.XML_KEY_RULE_KEY)
        #     self.rule_key_list.append(rule_key)
        #     print("rule_key = %s ,  rule_data = %s" % (rule_key, rule_data))

    def get_value(self, data, key):
        return self.get_node(data, key).text

    @staticmethod
    def get_node(data, key):
        if data is None:
            return None

        node = data.find(XMLKey.filter_with_key(key), XMLKey.XML_PATH_MAP)
        return node


    def valid_data(self):
        if self.root is None:
            return False
        else:
            return True
