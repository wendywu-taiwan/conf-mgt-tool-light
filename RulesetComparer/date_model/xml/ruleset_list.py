from RulesetComparer.date_model.xml.base import BaseModel
from RulesetComparer.properties import xmlKey as XMLKey


class RuleListModel(BaseModel):
    def __init__(self, xml):
        BaseModel.__init__(self, xml)
        self.rulesNameList = []
        self.rulesInfoMap = {}
        self.parse_data_catch_error()

    def parse_data(self):
        root = self.parse_xml_from_string()

        # get data array in <Rule></Rule>
        for rule in self.nodes_data(root_data=root, saxif_tag=True, key=XMLKey.NODE_KEY_RULE):
            # get data object in
            # <Context>
            #   <OrganizationId></OrganizationId>
            # </Context>
            rules_name = self.nest_node_value_data(data=rule,
                                                   saxif_tag=True,
                                                   node_key=XMLKey.NODE_KEY_CONTEXT,
                                                   value_key=XMLKey.ORGANIZATION_ID)
            self.rulesNameList.append(rules_name)

    def get_rules_file_name_list(self):
        return self.rulesNameList
