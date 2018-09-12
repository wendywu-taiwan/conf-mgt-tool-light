from RulesetComparer.dataModel.xml.baseModel import BaseModel
from RulesetComparer.properties import xmlKey as XMLKey


class RuleListModel(BaseModel):
    def __init__(self, xml):
        BaseModel.__init__(self, xml)
        self.root = self.parse_xml_from_string()

        self.rulesNameList = []
        self.parse_data()

    def parse_data(self):
        if not self.valid_data():
            return

        # get data array in <Rule></Rule>
        for rule in self.node_array(self.root, XMLKey.NODE_KEY_RULE):
            # get data object in
            # <Context>
            #   <OrganizationId></OrganizationId>
            # </Context>
            rules_name = self.value_in_node(rule,
                                            XMLKey.NODE_KEY_CONTEXT,
                                            XMLKey.ORGANIZATION_ID)
            self.rulesNameList.append(rules_name)

    def get_rules_file_name_list(self):
        return self.rulesNameList
