from django.conf import settings

from RulesetComparer.b2bRequestTask.downloadCompareRuleListTask import DownloadCompareRuleListTask as BaseCompareTask
from RulesetComparer.utils.ruleListComparer import RuleListComparer
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.dataModel.xml.rulesModel import RulesModel as ParseRuleModel
from RulesetComparer.dataModel.serializerModel.ruleListItemModel import  RuleListItemModel
from RulesetComparer.models import Environment, Country
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.gitManager import GitManager


class CompareWithGitRuleListTask(BaseCompareTask):

    def __init__(self, base_env_id, compare_env_id, country_id):
        # self.compare_hash_key = hash(self)
        self.compare_hash_key = 284291413
        self.baseEnv = Environment.objects.get(id=base_env_id)
        self.comparedEnv = Environment.objects.get(id=compare_env_id)
        self.country = Country.objects.get(id=country_id)
        self.add_rule_list = list()
        self.minus_rule_list = list()
        self.modify_rule_list = list()
        self.normal_rule_list = list()
        self._check_git_status()
        self.execute()

    @staticmethod
    def _check_git_status():
        manager = GitManager(settings.LOCAL_INT1_GIT_BRE_RULE_SET_REPOSITORY, settings.GIT_BRANCH_DEVELOP)
        if manager.status == GitManager.STATUS_NEED_PULL:
            manager.pull()

    def is_base_git(self):
        if self.baseEnv.name == 'Git':
            return True
        return False

    def __load_git_rule_set(self, rule_set_name):
        # save file to specific path
        file_path = settings.GIT_RULESET_SAVED_PATH % (settings.LOCAL_INT1_GIT_BRE_RULE_SET_REPOSITORY_NAME,
                                                       self.country.name)

        file_name_with_path = settings.RULESET_SAVED_NAME % (file_path,
                                                             rule_set_name)
        rule_set_file = fileManager.load_file(file_name_with_path)
        rules_module = ParseRuleModel(rule_set_file)
        return rules_module

    def __parse_add_list(self, add_list):
        for rule_name in add_list:
            if self.is_base_git() is True:
                rule_module = self.__load_rule_set(self.comparedEnv, rule_name)
            else:
                rule_module = self.__load_git_rule_set(rule_name)
            rule_list_item_parser = RuleListItemModel()
            rule_list_item_parser.set_add_rule(rule_module)
            self.add_rule_list.append(rule_list_item_parser.get_data())

    def __parse_minus_list(self, minus_list):
        for rule_name in minus_list:
            if self.is_base_git() is True:
                rule_module = self.__load_git_rule_set(rule_name)
            else:
                rule_module = self.__load_rule_set(self.comparedEnv, rule_name)

            rule_list_item_parser = RuleListItemModel()
            rule_list_item_parser.set_minus_rule(rule_module)
            self.minus_rule_list.append(rule_list_item_parser.get_data())

    def __parse_normal_and_modify_list(self, union_list):
        for rule_name in union_list:
            if self.is_base_git() is True:
                base_rules_module = self.__load_git_rule_set(rule_name)
                compared_rules_module = self.__load_rule_set(self.baseEnv, rule_name)
            else:
                base_rules_module = self.__load_rule_set(self.baseEnv, rule_name)
                compared_rules_module = self.__load_git_rule_set(rule_name)

            comparer = RulesetComparer(base_rules_module, compared_rules_module)
            rule_list_item_parser = RuleListItemModel()
            if comparer.no_difference():
                rule_list_item_parser.set_normal_rule(base_rules_module)
                self.normal_rule_list.append(rule_list_item_parser.get_data())
            else:
                rule_list_item_parser.set_modify_rule(rule_name,
                                                      base_rules_module.get_rules_count(),
                                                      compared_rules_module.get_rules_count(),
                                                      comparer.get_compare_key_count(),
                                                      comparer.get_base_key_count(),
                                                      comparer.get_difference_count())
                self.modify_rule_list.append(rule_list_item_parser.get_data())

    def execute(self):
        file_path = settings.GIT_RULESET_SAVED_PATH % (settings.LOCAL_INT1_GIT_BRE_RULE_SET_REPOSITORY_NAME,
                                                       self.country.name)

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


        # self.download_rules(self.baseEnv, base_rule_list)
        # self.download_rules(self.comparedEnv, compare_rule_list)

        comparer = RuleListComparer(base_rule_list, compare_rule_list)
        add_list = comparer.get_compare_rules_list()
        minus_list = comparer.get_base_rules_list()
        union_list = comparer.get_union_list()

        self.__parse_add_list(add_list)
        self.__parse_minus_list(minus_list)
        self.__parse_normal_and_modify_list(union_list)