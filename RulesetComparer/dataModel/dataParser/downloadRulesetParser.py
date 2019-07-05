from RulesetComparer.b2bRequestTask.downloadRulesetsTask import DownloadRulesetsTask
from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.utils import timeUtil
from RulesetComparer.utils.gitManager import GitManager


class DownloadRulesetParser:

    def __init__(self, json_data):
        try:
            self.environment = Environment.objects.get(id=json_data[KEY_ENVIRONMENT_ID])
            self.country = Country.objects.get(id=json_data[KEY_COUNTRY_ID])
            self.backup_key = json_data.get(KEY_BACKUP_KEY)
            self.compare_hash_key = json_data.get(KEY_COMPARE_HASH_KEY)
            self.backup_folder = json_data.get(KEY_BACKUP_FOLDER)
            self.ruleset_resource_path = None
            self.rule_name_list = []
            self.rule_name_xml_list = []
            self.parse_ruleset_type()

            if KEY_RULESET_NAME in json_data:
                self.parse_ruleset(json_data[KEY_RULESET_NAME])
            elif RULESET_NAME_LIST in json_data:
                self.parse_rulesets(json_data[RULESET_NAME_LIST])
        except BaseException as e:
            raise e

    def parse_ruleset_type(self):
        if self.backup_key is not '':
            if self.backup_folder == ENVIRONMENT_SOURCE:
                self.ruleset_resource_path = get_backup_path_applied_version(self.backup_key)
            else:
                self.ruleset_resource_path = get_backup_path_server_version(self.backup_key)
        elif self.environment.name == GIT_NAME:
            # update git ruleset
            GitManager(get_ruleset_git_root_path(), settings.GIT_BRANCH_DEVELOP).pull()
            self.ruleset_resource_path = get_rule_set_git_path(self.country.name)
        else:
            if self.compare_hash_key is None:
                self.compare_hash_key = hash(timeUtil.get_current_timestamp())
                # download ruleset from server
                DownloadRulesetsTask(self.environment.id, self.country.id, self.rule_name_list, self.compare_hash_key)
            self.ruleset_resource_path = get_rule_set_path(self.environment.name, self.country.name, self.compare_hash_key)

    def parse_ruleset(self, rule_name):
        suffix = FILE_NAME.get("_xml")
        name_with_suffix = suffix % rule_name
        self.rule_name_list.append(rule_name)
        self.rule_name_xml_list.append(name_with_suffix)

    def parse_rulesets(self, rule_list):
        for rule_name in rule_list:
            self.parse_ruleset(rule_name)
