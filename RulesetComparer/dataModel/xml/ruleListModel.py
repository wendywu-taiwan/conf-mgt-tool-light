from RulesetComparer.dataModel.xml.baseModel import BaseModel
from RulesetComparer.resource import xmlKey as XMLKey


class RuleListModel(BaseModel):
    def __init__(self, xml):
        BaseModel.__init__(self, xml)
        self.rule_key_list = []
        self.parse_xml_from_string()

    def parse_data(self):
        if not self.valid_data():
            return

        # get data array in <Rule></Rule>
        for rule_data in self.get_node_array(self.root, XMLKey.XML_KEY_RULE):
            # get data object in <Context></Context>
            context = self.get_node(rule_data, XMLKey.XML_KEY_CONTEXT)
            # get value in <OrganizationId></OrganizationId>
            rule_key = self.get_value(context, XMLKey.XML_KEY_ORGANIZATIONID)
            self.rule_key_list.append(rule_key)

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

    def get_rule_key_list(self):
        return self.rule_key_list
