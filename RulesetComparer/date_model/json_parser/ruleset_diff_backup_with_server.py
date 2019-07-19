from RulesetComparer.task.download_ruleset import DownloadRulesetTask
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.models import RulesetLogGroup


class RulesetDiffBackupWithServerParser:
    def __init__(self, backup_key, backup_folder, ruleset_name):
        try:
            self.ruleset_log_group = RulesetLogGroup.objects.get(backup_key=backup_key)
            self.backup_key = backup_key
            self.backup_folder = backup_folder
            self.ruleset_name = ruleset_name
            self.country = Country.objects.get(id=self.ruleset_log_group.country_id)
            self.environment = None
            self.backup_ruleset_xml = None
            self.server_ruleset_xml = None
            self.parse_ruleset_xml()
        except Exception as e:
            raise e

    def parse_ruleset_xml(self):
        if self.backup_folder == ENVIRONMENT_SOURCE:
            self.backup_ruleset_xml = load_backup_applied_version_rs(self.backup_key, self.ruleset_name)
        else:
            self.backup_ruleset_xml = load_backup_server_version_rs(self.backup_key, self.ruleset_name)

        self.environment = Environment.objects.get(id=self.ruleset_log_group.target_environment_id)
        download_task = DownloadRulesetTask(self.environment.id, self.country.id, self.ruleset_name, compare_hash_key=None)
        if download_task.success:
            self.server_ruleset_xml = download_task.get_ruleset_xml()
