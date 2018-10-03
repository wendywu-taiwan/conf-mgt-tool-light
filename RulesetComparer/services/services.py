from RulesetComparer.b2bRequestTask.downloadRuleSetTask import DownloadRuleSetTask
from RulesetComparer.b2bRequestTask.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.b2bRequestTask.downloadCompareRuleListTask import DownloadCompareRuleListTask as RuleListItemTask
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils import rulesetUtil
from RulesetComparer.dataModel.dataBuilder.rulesCompareBuilder import RulesCompareModel
from RulesetComparer.dataModel.xml.ruleSetParser import RulesModel as ParseRuleModel
from RulesetComparer.serializers.serializers import RuleSerializer


class RuleSetService(object):
    @staticmethod
    def get_rule_list_from_b2b(environment, country):
        task = DownloadRuleListTask(environment, country)
        return task

    @staticmethod
    def get_rule_from_b2b(environment, country, rule_set_name):
        task = DownloadRuleSetTask(environment, country, rule_set_name)

        ruleset = task.get_rule_set_file()
        rules_model = ParseRuleModel(ruleset)
        rule_data = RuleSerializer(rules_model.get_rules_data_array())
        return rule_data

    @staticmethod
    def compare_rule_list_rule_set(base_env_id, compare_env_id, country_id):
        task = RuleListItemTask(base_env_id, compare_env_id, country_id)
        return task

    @staticmethod
    def diff_rule_set(base_env_id, compare_env_id, country_id, compare_key, rule_set_name):
        base_rule = rulesetUtil.load_local_rule_file_with_id(base_env_id, country_id,
                                                             compare_key, rule_set_name)
        compare_rule = rulesetUtil.load_local_rule_file_with_id(compare_env_id, country_id,
                                                                compare_key, rule_set_name)

        base_module = ParseRuleModel(base_rule)
        compare_module = ParseRuleModel(compare_rule)

        comparer = RulesetComparer(base_module, compare_module)
        data = comparer.get_diff_data()
        return data

    @staticmethod
    def download_rule_set_from_git(country):
        pass

    @staticmethod
    def compare_rule_set(env1, env2, country, rule_set_name):
        task1 = DownloadRuleSetTask(env1, country, rule_set_name)
        task2 = DownloadRuleSetTask(env2, country, rule_set_name)

        rules_module1 = ParseRuleModel(task1.get_rule_set_file())
        rules_module2 = ParseRuleModel(task2.get_rule_set_file())

        comparer = RulesetComparer(rules_module1, rules_module2)
        response_model = RulesCompareModel(env1, env2, rule_set_name, comparer)

        return response_model

    @staticmethod
    def get_detail_rule_data(env_id, country_id, compare_key, rule_set_name):
        rule_set_file = rulesetUtil.load_local_rule_file_with_id(env_id,
                                                                 country_id,
                                                                 compare_key,
                                                                 rule_set_name)
        rules_module = ParseRuleModel(rule_set_file)
        return rules_module

