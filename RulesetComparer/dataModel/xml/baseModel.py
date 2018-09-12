import xml.etree.ElementTree as ET
import abc
from RulesetComparer.properties import xmlKey as XMLKey


class BaseModel:
    def __init__(self, xml):
        self.xml = xml
        self.root = None

    def parse_xml_from_string(self):
        if self.valid_data():

            return ET.fromstring(self.xml)

    def parse_xml_from_file(self):
        if self.valid_data():
            xml_tree = ET.parse(self.xml)
            return xml_tree.getroot()

    @staticmethod
    def node_array(data, key):
        return data.findall(XMLKey.filter_with_key(key),
                            XMLKey.XML_PATH_MAP)

    @staticmethod
    def node(data, node_key):
        if data is None:
            return None

        node = data.find(XMLKey.filter_with_key(node_key),
                         XMLKey.XML_PATH_MAP)
        return node

    def value(self, data, key):
        value_node = self.node(data, key)

        if value_node is None:
            return ""
        else:
            return value_node.text

    def value_in_node(self, data, node_key, key):
        if data is None:
            return None

        node = self.node(data, node_key)
        if node is None:
            return None

        return self.value(node, key)

    def valid_data(self):
        if self.xml is None:
            return False
        else:
            return True

    @abc.abstractmethod
    def parse_data(self):
        pass

