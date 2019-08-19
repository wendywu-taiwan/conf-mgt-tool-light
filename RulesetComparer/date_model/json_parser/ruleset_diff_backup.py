from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.models import RulesetLogGroup


class RulesetDiffBackupParser:
    def __init__(self, backup_key, ruleset_name):
        try:
            self.ruleset_log_group = RulesetLogGroup.objects.get(backup_key=backup_key)
            self.source_environment = Environment.objects.get(id=self.ruleset_log_group.source_environment_id)
            self.target_environment = Environment.objects.get(id=self.ruleset_log_group.target_environment_id)
            self.country = Country.objects.get(id=self.ruleset_log_group.country_id)
            self.backup_key = backup_key
            self.ruleset_name = ruleset_name
            self.source_ruleset_xml = load_backup_applied_version_rs(self.backup_key, self.ruleset_name)
            self.target_ruleset_xml = load_backup_server_version_rs(self.backup_key, self.ruleset_name)
        except Exception as e:
            raise e
