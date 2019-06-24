from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.b2bRequestTask.downloadRulesetTask import DownloadRulesetTask


class DiffBackupRulesetParser:
    JSON_KEY_ENV_ID = "environment_id"
    JSON_KEY_COUNTRY_ID = "country_id"
    JSON_KEY_BACKUP_KEY = "backup_key"
    JSON_KEY_RULESET_NAME = "ruleset_name"

    def __init__(self, json_data):
        try:
            self.environment = Environment.objects.get(id=json_data[self.JSON_KEY_ENV_ID])
            self.country = Country.objects.get(id=json_data[self.JSON_KEY_COUNTRY_ID])
            self.backup_key = json_data[self.JSON_KEY_BACKUP_KEY]
            self.ruleset_name = json_data[self.JSON_KEY_RULESET_NAME]
            self.backup_ruleset_xml = self.load_backup_ruleset_xml()
            self.server_ruleset_xml = self.load_server_ruleset_xml()
        except Exception as e:
            raise e

    def load_backup_ruleset_xml(self):
        return load_backup_server_version_rs(self.backup_key, self.ruleset_name)

    def load_server_ruleset_xml(self):
        download_task = DownloadRulesetTask(self.environment.id,
                                            self.country.id,
                                            self.ruleset_name,
                                            compare_hash_key=None)
        if download_task.success:
            return download_task.get_ruleset_xml()
        else:
            return None
