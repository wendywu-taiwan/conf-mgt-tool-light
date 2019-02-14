import xml.etree.ElementTree as ET
import abc
from RulesetComparer.properties import xmlKey as XMLKey


class BaseModel:
    def __init__(self, xml):
        self.xml = xml
        self.root = None
        self.has_xml_tag = True

    def parse_xml_from_string(self):
        if self.valid_data():
            return ET.fromstring(self.xml)

    def parse_xml_from_file(self):
        if self.valid_data():
            xml_tree = ET.parse(self.xml)
            return xml_tree.getroot()

    @staticmethod
    def node_array_with_xml(data, key):
        return data.findall(XMLKey.filter_with_key(key),
                            XMLKey.XML_PATH_MAP)

    @staticmethod
    def node_with_xml(data, node_key):
        if data is None:
            return None

        node = data.find(XMLKey.filter_with_key(node_key),
                         XMLKey.XML_PATH_MAP)
        return node

    def value_in_node_with_xml(self, data, node_key, value_key):
        if data is None:
            return ""

        node = self.node_with_xml(data, node_key)
        if node is None:
            return ""

        return self.value_with_xml(node, value_key)

    def value_with_xml(self, data, key):
        value_node = self.node_with_xml(data, key)

        if value_node is None:
            return ""
        elif value_node.text is None:
            return ""
        else:
            return value_node.text

    @staticmethod
    def node_array(data, array_path):
        return data.findall("./" + array_path)

    @staticmethod
    def node(data, node_path):
        if data is None:
            return None

        node = data.find("./" + node_path)
        if node is None:
            node = data.find("./" + node_path.lower())

        return node

    def value(self, data, node_path):
        value_node = self.node(data, node_path)

        if value_node is None:
            return ""
        elif value_node.text is None:
            return ""
        else:
            return value_node.text

    def valid_data(self):
        if self.xml is None:
            return False
        else:
            return True

    def check_xml_tag(self):
        if len(self.node_array_with_xml(self.root, XMLKey.NODE_KEY_RULE)) > 0:
            self.has_xml_tag = True
        else:
            self.has_xml_tag = False

    @abc.abstractmethod
    def parse_data(self):
        pass
