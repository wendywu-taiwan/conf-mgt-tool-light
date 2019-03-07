from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.utils import timeUtil


class DownloadRulesetParser:
    JSON_KEY_ENV_ID = "environment_id"
    JSON_KEY_COUNTRY_ID = "country_id"
    JSON_KEY_RULESET_NAME = "ruleset_name"
    JSON_KEY_RULESET_NAME_LIST = "ruleset_name_list"
    JSON_KEY_COMPARE_HASH_KEY = "compare_hash_key"

    def __init__(self, json_data):
        try:
            self.environment = Environment.objects.get(id=json_data[self.JSON_KEY_ENV_ID])
            self.country = Country.objects.get(id=json_data[self.JSON_KEY_COUNTRY_ID])
            self.rule_name_list = []
            self.rule_name_xml_list = []
            if self.JSON_KEY_COMPARE_HASH_KEY in json_data:
                self.compare_hash_key = json_data[self.JSON_KEY_COMPARE_HASH_KEY]
                self.ruleset_exist = True
            else:
                self.compare_hash_key = hash(timeUtil.get_current_timestamp())
                self.ruleset_exist = False

            if self.JSON_KEY_RULESET_NAME in json_data:
                self.parse_ruleset(json_data[self.JSON_KEY_RULESET_NAME])
            elif self.JSON_KEY_RULESET_NAME_LIST in json_data:
                self.parse_rulesets(json_data[self.JSON_KEY_RULESET_NAME_LIST])
        except BaseException as e:
            raise e

    def parse_ruleset(self, rule_name):
        suffix = FILE_NAME.get("_xml")
        name_with_suffix = suffix % rule_name
        self.rule_name_list.append(rule_name)
        self.rule_name_xml_list.append(name_with_suffix)

    def parse_rulesets(self, rule_list):
        for rule_name in rule_list:
            self.parse_ruleset(rule_name)
