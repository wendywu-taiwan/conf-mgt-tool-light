from RulesetComparer.b2bRequestTask.downloadRuleSetTask import DownloadRuleSetTask
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.models import Country, Environment
from RulesetComparer.dataModel.xml.rulesModel import RulesModel as ParseRuleModel
from RulesetComparer.dataModel.serializerModel.ruleListItemModel import  RuleListItemModel
from RulesetComparer.utils.ruleListComparer import RuleListComparer
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils import fileManager
from django.conf import settings


class DownloadCompareRuleListTask:

    def __init__(self, base_env_id, compare_env_id, country_id):
        # self.compare_hash_key = hash(self)
        self.compare_hash_key = -9223372036577735175
        self.baseEnv = Environment.objects.get(id=base_env_id)
        self.comparedEnv = Environment.objects.get(id=compare_env_id)
        self.country = Country.objects.get(id=country_id)
        self.add_rule_list = list()
        self.minus_rule_list = list()
        self.modify_rule_list = list()
        self.normal_rule_list = list()
        self.execute()

    def __load_rule_set(self, env, rule_set_name):
        # save file to specific path
        file_path = settings.RULESET_SAVED_PATH % (env.name,
                                                   self.country.name,
                                                   self.compare_hash_key)

        file_name_with_path = settings.RULESET_SAVED_NAME % (file_path,
                                                             rule_set_name)
        rule_set_file = fileManager.load_file(file_name_with_path)
        rules_module = ParseRuleModel(rule_set_file)
        return rules_module

    def execute(self):
        base_rule_list_task = DownloadRuleListTask(self.baseEnv.id, self.country.id)
        compare_rule_list_task = DownloadRuleListTask(self.comparedEnv.id, self.country.id)

        base_rule_list = base_rule_list_task.get_rule_list()
        compare_rule_list = compare_rule_list_task.get_rule_list()

        # self.download_rules(self.baseEnv, base_rule_list)
        # self.download_rules(self.comparedEnv, compare_rule_list)

        comparer = RuleListComparer(base_rule_list, compare_rule_list)
        add_list = comparer.get_compare_rules_list()
        minus_list = comparer.get_base_rules_list()
        union_list = comparer.get_union_list()

        for rule_name in add_list:
            rule_module = self.__load_rule_set(self.comparedEnv, rule_name)
            rule_list_item_parser = RuleListItemModel()
            rule_list_item_parser.set_add_rule(rule_module)
            self.add_rule_list.append(rule_list_item_parser.get_data())

        for rule_name in minus_list:
            rule_module = self.__load_rule_set(self.baseEnv, rule_name)
            rule_list_item_parser = RuleListItemModel()
            rule_list_item_parser.set_minus_rule(rule_module)
            self.minus_rule_list.append(rule_list_item_parser.get_data())

        for rule_name in union_list:
            base_rules_module = self.__load_rule_set(self.baseEnv, rule_name)
            compared_rules_module = self.__load_rule_set(self.comparedEnv, rule_name)

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

    def get_add_rule_list(self):
        return self.add_rule_list

    def get_minus_rule_list(self):
        return self.minus_rule_list

    def get_modify_rule_list(self):
        return self.modify_rule_list

    def get_normal_rule_list(self):
        return self.normal_rule_list

    def download_rules(self, env, rule_list):
        for rule_name in rule_list:
            DownloadRuleSetTask(env.name, self.country.name,
                                rule_name, self.compare_hash_key)


