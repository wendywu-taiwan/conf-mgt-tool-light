from RulesetComparer.b2bRequestTask.downloadRuleSetTask import DownloadRuleSetTask
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.models import Country, Environment
from RulesetComparer.dataModel.xml.ruleSetParser import RulesModel as ParseRuleModel
from RulesetComparer.dataModel.dataBuilder.ruleListItemBuilder import RuleListItemBuilder
from RulesetComparer.utils.ruleListComparer import RuleListComparer
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.utils import fileManager, rulesetUtil
from RulesetComparer.properties import dataKey as key
from RulesetComparer.properties import config
from RulesetComparer.properties.config import get_rule_set_git_path
from django.conf import settings


class CompareRuleListTask:

    def __init__(self, base_env_id, compare_env_id, country_id):
        # self.compare_hash_key = hash(self)
        self.compare_hash_key = 284291413
        self.baseEnv = Environment.objects.get(id=base_env_id)
        self.comparedEnv = Environment.objects.get(id=compare_env_id)
        self.country = Country.objects.get(id=country_id)

        # list for saving rule in compared env but not in base env
        self.add_rule_list = list()
        # list for saving rule in base env but not in compared env
        self.remove_rule_list = list()
        # list for saving rule has different version in base and compared env
        self.modify_rule_list = list()
        # list for saving rule has same version in base and compared env
        self.normal_rule_list = list()

        # map for saving rule details for each rule file.
        # key = rule file name
        # value = rule list
        self.rule_detail_map = {}

        # map for saving rule diff result for each rule file.
        # key = rule file name
        # value = rule diff list
        self.rule_diff_map = {}

        # check if environment is git
        self.git_environment = self.check_git_environment()

        self.check_git_status()
        self.execute()

    def check_git_environment(self):
        if self.baseEnv.name == key.ENVIRONMENT_KEY_GIT:
            return key.BASE_ENVIRONMENT_GIT
        elif self.comparedEnv.name == key.ENVIRONMENT_KEY_GIT:
            return key.COMPARE_ENVIRONMENT_GIT
        else:
            return key.NO_ENVIRONMENT_GIT

    def check_git_status(self):
        if self.git_environment == key.NO_ENVIRONMENT_GIT:
            return

        path = get_rule_set_git_path("")
        manager = GitManager(path, settings.GIT_BRANCH_DEVELOP)
        if manager.status == GitManager.STATUS_NEED_PULL:
            manager.pull()

    def execute(self):
        if self.git_environment == key.BASE_ENVIRONMENT_GIT:
            base_rule_list = self.updated_rule_list_from_git()
            compare_rule_list = self.updated_rule_list_from_server(self.comparedEnv)
        elif self.git_environment == key.COMPARE_ENVIRONMENT_GIT:
            base_rule_list = self.updated_rule_list_from_server(self.baseEnv)
            compare_rule_list = self.updated_rule_list_from_git()
        else:
            base_rule_list = self.updated_rule_list_from_server(self.baseEnv)
            compare_rule_list = self.updated_rule_list_from_server(self.comparedEnv)

        comparer = RuleListComparer(base_rule_list, compare_rule_list)
        add_list = comparer.get_compare_rules_list()
        minus_list = comparer.get_base_rules_list()
        union_list = comparer.get_union_list()

        self.parse_add_list_rule(add_list)
        self.parse_remove_list_rule(minus_list)
        self.parse_union_list_rule(union_list)

    def updated_rule_list_from_server(self, environment):
        updated_list = DownloadRuleListTask(environment.id, self.country.id).get_rule_list()
        # self.download_rules(environment, updated_list)
        return updated_list

    def updated_rule_list_from_git(self):
        git_file_path = get_rule_set_git_path(self.country.name)
        return fileManager.get_rule_name_list(git_file_path)

    def download_rules(self, env, rule_list):
        for rule_name in rule_list:
            DownloadRuleSetTask(env.id, self.country.id, rule_name, self.compare_hash_key)

    def parse_add_list_rule(self, add_list):
        for rule_name in add_list:
            rule_module = self.load_rule_module(self.comparedEnv, rule_name)
            rule_list_item_parser = RuleListItemBuilder(rule_module, self.compare_hash_key)
            rule_list_item_parser.set_add_rule()
            self.add_rule_list.append(rule_list_item_parser.get_data())
            self.rule_detail_map[rule_name] = rule_module.get_rules_data_array()

    def parse_remove_list_rule(self, remove_list):
        for rule_name in remove_list:
            rule_module = self.load_rule_module(self.baseEnv, rule_name)
            rule_list_item_parser = RuleListItemBuilder(rule_module, self.compare_hash_key)
            rule_list_item_parser.set_remove_rule()
            self.remove_rule_list.append(rule_list_item_parser.get_data())
            self.rule_detail_map[rule_name] = rule_module.get_rules_data_array()

    def parse_union_list_rule(self, union_list):
        for rule_name in union_list:
            base_rules_module = self.load_rule_module(self.baseEnv, rule_name)
            compared_rules_module = self.load_rule_module(self.comparedEnv, rule_name)

            comparer = RulesetComparer(base_rules_module, compared_rules_module)
            rule_list_item_parser = RuleListItemBuilder(base_rules_module, self.compare_hash_key)
            if comparer.no_difference():
                rule_list_item_parser.set_normal_rule()
                self.normal_rule_list.append(rule_list_item_parser.get_data())
                self.rule_detail_map[rule_name] = base_rules_module.get_rules_data_array()
            else:
                rule_list_item_parser.set_modify_rule(base_rules_module.get_rules_count(),
                                                      compared_rules_module.get_rules_count(),
                                                      comparer.get_compare_key_count(),
                                                      comparer.get_base_key_count(),
                                                      comparer.get_difference_count())
                self.modify_rule_list.append(rule_list_item_parser.get_data())
                self.rule_diff_map[rule_name] = comparer.get_diff_data()

    def load_rule_module(self, env, rule_name):
        if env.name == config.GIT.get("environment_name"):
            rule_set_file = rulesetUtil.load_git_file_with_name(self.country.name, rule_name)
        else:
            rule_set_file = rulesetUtil.load_rule_file_with_name(env.name,
                                                                 self.country.name,
                                                                 self.compare_hash_key,
                                                                 rule_name)
        rules_module = ParseRuleModel(rule_set_file)
        return rules_module

    def get_add_rule_list(self):
        return self.add_rule_list

    def get_remove_rule_list(self):
        return self.remove_rule_list

    def get_modify_rule_list(self):
        return self.modify_rule_list

    def get_normal_rule_list(self):
        return self.normal_rule_list

    def get_rule_detail_map(self):
        return self.rule_detail_map

    def get_rule_diff_map(self):
        return self.rule_diff_map


