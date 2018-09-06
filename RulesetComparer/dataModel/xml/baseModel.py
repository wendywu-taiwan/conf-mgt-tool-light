import xml.etree.ElementTree as ET
import abc
from RulesetComparer.resource import xmlKey as XMLKey


class BaseModel:
    def __init__(self, xml):
        self.xml = xml
        self.root = None

    def parse_xml_from_string(self):
        self.root = ET.fromstring(self.xml)
        self.parse_data()

    def parse_xml_from_file(self):
        xml_tree = ET.parse(self.xml)
        self.root = xml_tree.getroot()
        self.parse_data()

    @staticmethod
    def get_node_array(data, key):
        return data.findall(XMLKey.filter_with_key(key),
                            XMLKey.XML_PATH_MAP)

    @staticmethod
    def get_node(data, key):
        if data is None:
            return None

        node = data.find(XMLKey.filter_with_key(key), XMLKey.XML_PATH_MAP)
        return node

    def get_value(self, data, key):
        return self.get_node(data, key).text

    def valid_data(self):
        if self.root is None:
            return False
        else:
            return True

    @abc.abstractmethod
    def parse_data(self):
        pass

