from abc import abstractmethod


class BaseApplyRulesetParser:
    def __init__(self):
        try:
            self.source_environment = None
            self.target_environment = None
            self.country = None
            self.backup_key = None
            self.ruleset_path = None
            self.rulesets = []
            self.parse_ruleset_data()
        except BaseException as e:
            raise e

    @abstractmethod
    def parse_ruleset_data(self):
        pass
