from RulesetComparer.date_model.ruleset_loader.base import BaseRulesetLoader
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.models import RulesetLogGroup


class BackupRulesetLoader(BaseRulesetLoader):
    def __init__(self, backup_key, folder_name, ruleset_name):
        try:
            BaseRulesetLoader.__init__(self)
            self.backup_key = backup_key
            self.folder_name = folder_name
            self.ruleset_name = ruleset_name
            self.is_applied_version = self.parse_folder_name()
            self.log_group = RulesetLogGroup.objects.get(backup_key=backup_key)
            self.parse_environment()
            self.parse_country()
            self.__load_ruleset__()
        except Exception as e:
            raise e

    def parse_folder_name(self):
        if self.folder_name == ENVIRONMENT_SOURCE:
            return True
        else:
            return False

    def parse_environment(self):
        if self.is_applied_version:
            self.environment = Environment.objects.get(id=self.log_group.source_environment_id)
        else:
            self.environment = Environment.objects.get(id=self.log_group.target_environment_id)

    def parse_country(self):
        self.country = Country.objects.get(id=self.log_group.country_id)

    def __parse_ruleset_path__(self):
        if self.is_applied_version:
            self.ruleset_path = get_backup_path_applied_version(self.backup_key)
        else:
            self.ruleset_path = get_backup_path_server_version(self.backup_key)

    def __parse_ruleset_path_info__(self):
        self.ruleset_path_info[KEY_BACKUP_KEY] = self.backup_key
        self.ruleset_path_info[KEY_BACKUP_FOLDER] = self.folder_name
