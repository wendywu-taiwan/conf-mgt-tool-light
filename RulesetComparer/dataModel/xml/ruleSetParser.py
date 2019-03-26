from RulesetComparer.dataModel.xml.baseParser import BaseModel
from RulesetComparer.dataModel.xml.ruleParser import RuleModel
from RulesetComparer.dataModel.dataBuilder.ruleSetBuilder import RuleSetBuilder
from RulesetComparer.properties import xmlKey as XMLKey
from RulesetComparer.utils import logger
from lxml import etree


# this is for handling ruleset data, a ruleset file contains many rules
class RulesModel(BaseModel):
    def __init__(self, xml, rule_name):
        BaseModel.__init__(self, xml)
        self.root = None
        self.has_saxif_tag = False
        self.rulesName = rule_name
        self.rulesMap = {}
        self.parse_data_catch_error()

    def parse_data(self):
        root = self.parse_xml_from_file()

        if len(self.nodes_data(root, saxif_tag=True, key=XMLKey.NODE_KEY_RULE)) > 0:
            has_saxif_tag = True
        else:
            has_saxif_tag = False

        for rule in self.nodes_data(root, saxif_tag=has_saxif_tag,
                                    key=XMLKey.NODE_KEY_RULE,
                                    path=XMLKey.NODE_KEY_RULE):
            rule_model = RuleModel(rule, has_saxif_tag)
            rule_key = rule_model.combinedKey
            self.rulesMap[rule_key] = rule_model

    def remove_rule_xml(self, rule_combined_key):
        new_rulesets_xml = self.root
        for rule in self.nodes_data(new_rulesets_xml,
                                    saxif_tag=self.has_saxif_tag,
                                    key=XMLKey.NODE_KEY_RULE,
                                    path=XMLKey.NODE_KEY_RULE):
            rule_model = RuleModel(rule, self.has_saxif_tag)
            rule_key = rule_model.combinedKey
            if rule_combined_key == rule_key:
                self.root.remove(rule)
                logger.info_log("remove_rule_xml", etree.tostring(rule, pretty_print=True))

        logger.info_log("new_rulesets_xml", etree.tostring(self.root, pretty_print=True))

    def get_rule_by_key(self, combined_key):
        return self.rulesMap[combined_key]

    def get_rules_name(self):
        return self.rulesName

    def get_rules_count(self):
        return len(self.rulesMap.keys())

    def get_rule_combined_key_list(self):
        return list(self.rulesMap.keys())

    def get_rule_full_value(self, rule_key):
        rule = self.rulesMap[rule_key]

        if rule is None:
            return ""

        return rule.fullValue

    def get_rules_data_array(self, name_list=None):
        array = list()

        if name_list is None:
            name_list = self.get_rule_combined_key_list()

        for rule in name_list:
            rule_model = self.rulesMap[rule]
            if rule_model is None:
                continue
            data_builder = RuleSetBuilder(rule_model)
            array.append(data_builder.get_data())
        return array
