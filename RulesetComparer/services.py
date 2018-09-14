from RulesetComparer.apiRequestTask.b2b.downloadRuleSetTask import DownloadRuleSetTask
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.dataModel.responseModel.rulesCompareModel import RulesCompareModel
from RulesetComparer.apiRequestTask.b2b.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.utils.ruleListComparer import RuleListComparer
from RulesetComparer.dataModel.responseModel.ruleListCompareModel import RuleListCompareModel
from RulesetComparer.dataModel.xml.rulesModel import RulesModel as ParseRuleModel
from RulesetComparer.dataModel.responseModel.rulesModel import RulesModel as ResponseRulesModel


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
        response_model = ResponseRulesModel(rules_model)
        return response_model

    def compare_rule_list(self, environment1, environment2, country):
        rule_list_1 = self.get_rule_list_from_b2b(environment1, country).get_content()
        rule_list_2 = self.get_rule_list_from_b2b(environment2, country).get_content()
        comparer = RuleListComparer(rule_list_1, rule_list_2)
        response_model = RuleListCompareModel(environment1, environment2, comparer)
        return response_model

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
