from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.b2bRequestTask.downloadRulesetsTask import DownloadRulesetsTask


class DiffBackupRulesetParser:
    JSON_KEY_ENV_ID = "environment_id"
    JSON_KEY_COUNTRY_ID = "country_id"
    JSON_KEY_BACKUP_FOLDER_NAME = "backup_folder_name"
    JSON_KEY_RULESET_NAME = "ruleset_name"

    def __init__(self, json_data):
        try:
            self.environment = Environment.objects.get(id=json_data[self.JSON_KEY_ENV_ID])
            self.country = Country.objects.get(id=json_data[self.JSON_KEY_COUNTRY_ID])
            self.backup_folder_name = json_data[self.JSON_KEY_BACKUP_FOLDER_NAME]
            self.ruleset_name = json_data[self.JSON_KEY_RULESET_NAME]
            self.backup_ruleset_xml = self.load_backup_ruleset_xml()
            self.server_ruleset_xml = self.load_server_ruleset_xml()
        except Exception as e:
            raise e

    def load_backup_ruleset_xml(self):
        return load_backup_ruleset_with_name(self.environment.name,
                                             self.country.name,
                                             self.backup_folder_name,
                                             self.ruleset_name)

    def load_server_ruleset_xml(self):
        compare_hash_key = hash(timeUtil.get_current_timestamp())
        ruleset_array = [self.ruleset_name]
        download_task = DownloadRulesetsTask(self.environment.id, self.country.id, ruleset_array, compare_hash_key)
        return load_rule_file_with_id(self.environment.id, self.country.id, compare_hash_key, self.ruleset_name)
