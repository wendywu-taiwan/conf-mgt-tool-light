import traceback
from RulesetComparer.models import Country
from RulesetComparer.utils import timeUtil
from RulesetComparer.utils.logger import *
from RulesetComparer.properties.config import *


class DownloadRulesetParser:
    JSON_KEY_ENV_ID = "environment_id"
    JSON_KEY_COUNTRY_ID = "country_id"
    JSON_KEY_RULESET_NAME_LIST = "ruleset_name_list"

    def __init__(self, json_data):
        try:
            self.env_id = json_data[self.JSON_KEY_ENV_ID]
            self.country_id = json_data[self.JSON_KEY_COUNTRY_ID]
            self.ruleset_name_list = self.parse_ruleset(json_data[self.JSON_KEY_RULESET_NAME_LIST])
        except BaseException as e:
            traceback.print_exc()
            error_log(traceback.format_exc())
            raise e

    @staticmethod
    def parse_ruleset(rule_list):
        rule_name_list = []
        for rule_name in rule_list:
            suffix = FILE_NAME.get("_xml")
            name_with_suffix = suffix % rule_name
            rule_name_list.append(name_with_suffix)
        return rule_name_list
