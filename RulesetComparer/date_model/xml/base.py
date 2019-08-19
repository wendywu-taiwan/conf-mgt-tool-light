import xml.etree.ElementTree as ET
import abc
from RulesetComparer.properties import xml_key as XMLKey


class BaseModel:
    def __init__(self, xml):
        self.xml = xml

    def parse_data_catch_error(self):
        try:
            self.parse_data()
        except Exception as e:
            raise e

    def parse_xml_from_string(self):
        return ET.fromstring(self.xml)

    def parse_xml_from_file(self):
        xml_tree = ET.parse(self.xml)
        return xml_tree.getroot()

    @staticmethod
    # root_data:    <Rule>
    #                     <RuleType>FieldTranslation</RuleType>
    #                     <Key>root.task.basicClaimData.vehicle.vehicleAdmin.vehicleIdentificationId</Key>
    #                     <Value>EN=Chassis Number,DE=Chassis Number</Value>
    #                     <Status>Active</Status>
    #               </Rule>
    # key: Rule ->  <Rule></Rule>
    # path:Rule ->  ./Rule
    # return:       <RuleType>FieldTranslation</RuleType>
    #               <Key>root.task.basicClaimData.vehicle.vehicleAdmin.vehicleIdentificationId</Key>
    #               <Value>EN=Chassis Number,DE=Chassis Number</Value>
    #               <Status>Active</Status>
    def nodes_data(root_data, saxif_tag, key=None, path=None):
        if saxif_tag:
            # get nodes data <saxif_path:key> in <saxif_path:http://www.audatex.com/SAXIF>
            return root_data.findall(XMLKey.filter_with_key(key),
                                     XMLKey.XML_PATH_MAP)
        else:
            # get nodes data in path ./path
            return root_data.findall("./" + path)

    # data:      <Status>Active</Status>
    # node_key:  Status -> <Status></Status>
    # node_path: Status -> ./Status
    # return:    <Status>Active</Status>
    @staticmethod
    def node_data(data, saxif_tag, node_key=None, node_path=None):
        if data is None:
            return None

        if saxif_tag is True:
            node_data = data.find(XMLKey.filter_with_key(node_key),
                                  XMLKey.XML_PATH_MAP)
        else:
            node_data = data.find("./" + node_path)
            if node_data is None:
                node_data = data.find("./" + node_path.lower())

        return node_data

    # data:      <Status>Active</Status>
    # node key:  Status -> <Status></Status>
    # node path: Status -> ./Status
    # return:    Active
    def node_value_data(self, data, saxif_tag, node_key=None, node_path=None):
        if data is None:
            return ""

        node_data = self.node_data(data, saxif_tag, node_key=node_key, node_path=node_path)

        if node_data is None:
            return ""
        elif node_data.text is None:
            return ""
        else:
            return node_data.text

    # data:       <Context><Status>Active</Status></Context>
    # node_key:   Context -> <Context></Context>
    # value_key:  Status -> <Status></Status>
    # node_path:  Context/Status -> ./Context/Status
    # return:     Active
    def nest_node_value_data(self, data, saxif_tag, node_key=None, value_key=None, node_path=None):
        if data is None:
            return ""

        if saxif_tag is True:
            node_data = self.node_data(data, saxif_tag=saxif_tag, node_key=node_key)
            if node_data is None:
                return ""
            node_value_data = self.node_value_data(node_data, saxif_tag=saxif_tag, node_key=value_key)
        else:
            node_value_data = self.node_value_data(data, saxif_tag=saxif_tag, node_path=node_path)

        return node_value_data

    @abc.abstractmethod
    def parse_data(self):
        pass
