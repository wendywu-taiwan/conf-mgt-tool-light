from RulesetComparer.utils.rulesetUtil import *
import re


class ShowRulesetXMLParser:
    JSON_KEY_BACKUP_KEY = "backup_key"
    JSON_KEY_ENVIRONMENT_VERSION = "environment_version"
    JSON_KEY_RULESET_NAME = "ruleset_name"
    ENVIRONMENT_SOURCE = "source"
    ENVIRONMENT_TARGET = "target"

    def __init__(self, json_data):
        try:
            self.ruleset_name = json_data.get(self.JSON_KEY_RULESET_NAME)
            self.backup_key = json_data.get(self.JSON_KEY_BACKUP_KEY)
            self.is_applied_version = self.parse_environment_version(json_data.get(self.JSON_KEY_ENVIRONMENT_VERSION))
            self.ruleset_path = self.parse_ruleset_path()
            self.ruleset = None
            self.ruleset_array = None

            self.parse_ruleset()
        except BaseException as e:
            raise e

    def parse_environment_version(self, environment_version):
        if environment_version == self.ENVIRONMENT_SOURCE:
            return True
        else:
            return False

    def parse_ruleset_path(self):
        if self.is_applied_version:
            return get_rs_path_backup_applied_version(self.backup_key, self.ruleset_name)
        else:
            return get_rs_path_backup_server_version(self.backup_key, self.ruleset_name)

    def parse_ruleset(self):
        if self.ruleset_path is None:
            return ""

        if self.is_applied_version:
            self.ruleset = load_backup_applied_version_rs(self.backup_key, self.ruleset_name)
        else:
            self.ruleset = load_backup_server_version_rs(self.backup_key, self.ruleset_name)

        if "      <" in self.ruleset:
            ruleset_replace = self.ruleset.replace("      <", "level3\n<")
            ruleset_replace = ruleset_replace.replace("    <", "level2\n<")
            ruleset_replace = ruleset_replace.replace("  <", "level1\n<")
        else:
            ruleset_replace = self.ruleset.replace("   <", "level3\n<")
            ruleset_replace = ruleset_replace.replace("  <", "level2\n<")
            ruleset_replace = ruleset_replace.replace(" <", "level1\n<")

        self.ruleset_array = re.split('\n', ruleset_replace)
        return self.ruleset_array
