from abc import abstractmethod
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.date_model.xml.ruleSetObject import RulesetObject


class BaseRulesetLoader:
    def __init__(self):
        self.ruleset_name = None
        self.ruleset = None
        self.ruleset_path = None
        self.ruleset_model = None
        self.environment = None
        self.country = None
        self.ruleset_path_info = {}

    @abstractmethod
    def __parse_ruleset_path__(self):
        pass

    @abstractmethod
    def __parse_ruleset_path_info__(self):
        pass

    def __load_ruleset__(self):
        self.__parse_ruleset_path__()
        self.__parse_ruleset_path_info__()
        self.ruleset = load_rule_file_with_path(self.ruleset_path, self.ruleset_name)
        self.ruleset_model = RulesetObject(self.ruleset, self.ruleset_name)

    def get_ruleset(self):
        return self.ruleset

    def get_ruleset_model(self):
        return self.ruleset_model

    def get_ruleset_path_info(self):
        return self.ruleset_path_info
