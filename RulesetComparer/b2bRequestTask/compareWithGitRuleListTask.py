from django.conf import settings
from RulesetComparer.utils.ruleListComparer import RuleListComparer
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.dataModel.xml.ruleSetParser import RulesModel as ParseRuleModel
from RulesetComparer.dataModel.dataBuilder.ruleListItemBuilder import RuleListItemBuilder
from RulesetComparer.models import Environment, Country
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.properties import dataKey as key
from RulesetComparer.properties.config import get_rule_set_git_path
from RulesetComparer.utils import rulesetUtil


class CompareWithGitRuleListTask:

    def __init__(self, base_env_id, compare_env_id, country_id):
        # self.compare_hash_key = hash(self)
        self.compare_hash_key = 284291413
        self.baseEnv = Environment.objects.get(id=base_env_id)
        self.comparedEnv = Environment.objects.get(id=compare_env_id)
        self.country = Country.objects.get(id=country_id)
        self.add_rule_list = list()
        self.remove_rule_list = list()
        self.modify_rule_list = list()
        self.normal_rule_list = list()
        self._check_git_status()
        self.execute()

    @staticmethod
    def _check_git_status():
        path = get_rule_set_git_path("")
        manager = GitManager(path, settings.GIT_BRANCH_DEVELOP)
        if manager.status == GitManager.STATUS_NEED_PULL:
            manager.pull()

    def is_base_git(self):
        if self.baseEnv.name == key.ENVIRONMENT_KEY_GIT:
            return True
        return False

    def __load_rule_set(self, env, rule_set_name):
        rule_set_file = rulesetUtil.load_rule_file_with_name(env.name,
                                                             self.country.name,
                                                             self.compare_hash_key,
                                                             rule_set_name)
        rules_module = ParseRuleModel(rule_set_file)
        return rules_module

    def __load_git_rule_set(self, rule_set_name):
        rule_set_file = rulesetUtil.load_git_file_with_name(self.country.name, rule_set_name)
        rules_module = ParseRuleModel(rule_set_file)
        return rules_module

    def __parse_add_list(self, add_list):
        for rule_name in add_list:
            if self.is_base_git() is True:
                rule_module = self.__load_rule_set(self.comparedEnv, rule_name)
            else:
                rule_module = self.__load_git_rule_set(rule_name)

            rule_list_item_parser = RuleListItemBuilder(rule_module, self.compare_hash_key)
            rule_list_item_parser.set_add_rule()
            self.add_rule_list.append(rule_list_item_parser.get_data())

    def __parse_remove_list(self, remove):
        for rule_name in remove:
            if self.is_base_git() is True:
                rule_module = self.__load_git_rule_set(rule_name)
            else:
                rule_module = self.__load_rule_set(self.baseEnv, rule_name)

            rule_list_item_parser = RuleListItemBuilder(rule_module, self.compare_hash_key)
            rule_list_item_parser.set_remove_rule()
            self.remove_rule_list.append(rule_list_item_parser.get_data())

    def __parse_normal_and_modify_list(self, union_list):
        for rule_name in union_list:
            if self.is_base_git() is True:
                base_rules_module = self.__load_git_rule_set(rule_name)
                compared_rules_module = self.__load_rule_set(self.comparedEnv, rule_name)
            else:
                base_rules_module = self.__load_rule_set(self.baseEnv, rule_name)
                compared_rules_module = self.__load_git_rule_set(rule_name)

            comparer = RulesetComparer(base_rules_module, compared_rules_module)
            rule_list_item_parser = RuleListItemBuilder(base_rules_module, self.compare_hash_key)
            if comparer.no_difference():
                rule_list_item_parser.set_normal_rule()
                self.normal_rule_list.append(rule_list_item_parser.get_data())
            else:
                rule_list_item_parser.set_modify_rule(base_rules_module.get_rules_count(),
                                                      compared_rules_module.get_rules_count(),
                                                      comparer.get_compare_key_count(),
                                                      comparer.get_base_key_count(),
                                                      comparer.get_difference_count())
                self.modify_rule_list.append(rule_list_item_parser.get_data())

    def execute(self):
        file_path = get_rule_set_git_path(self.country.name)

        if self.is_base_git():
            base_rule_list = fileManager.get_rule_name_list(file_path)
            compare_rule_list = DownloadRuleListTask(self.comparedEnv.id,
                                                     self.country.id).get_rule_list()
            # self.download_rules(self.baseEnv, base_rule_list)
        else:
            base_rule_list = DownloadRuleListTask(self.baseEnv.id,
                                                  self.country.id).get_rule_list()
            compare_rule_list = fileManager.get_rule_name_list(file_path)
            # self.download_rules(self.comparedEnv, compare_rule_list)

        comparer = RuleListComparer(base_rule_list, compare_rule_list)
        add_list = comparer.get_compare_rules_list()
        remove_list = comparer.get_base_rules_list()
        union_list = comparer.get_union_list()

        self.__parse_add_list(add_list)
        self.__parse_remove_list(remove_list)
        self.__parse_normal_and_modify_list(union_list)

    def get_add_rule_list(self):
        return self.add_rule_list

    def get_remove_rule_list(self):
        return self.remove_rule_list

    def get_modify_rule_list(self):
        return self.modify_rule_list

    def get_normal_rule_list(self):
        return self.normal_rule_list
