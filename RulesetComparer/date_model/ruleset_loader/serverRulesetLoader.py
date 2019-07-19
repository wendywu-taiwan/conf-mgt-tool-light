from RulesetComparer.date_model.ruleset_loader.baseRulesetLoader import BaseRulesetLoader
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.models import Country, Environment


class ServerRulesetLoader(BaseRulesetLoader):
    def __init__(self, compare_key, env_id, country_id, ruleset_name):
        try:
            BaseRulesetLoader.__init__(self)
            self.compare_key = compare_key
            self.environment = Environment.objects.get(id=env_id)
            self.country = Country.objects.get(id=country_id)
            self.ruleset_name = ruleset_name
            BaseRulesetLoader.__load_ruleset__(self)
        except Exception as e:
            raise e

    def __parse_ruleset_path__(self):
        self.ruleset_path = get_rule_set_path(self.environment.name, self.country.name, self.compare_key)

    def __parse_ruleset_path_info__(self):
        self.ruleset_path_info[KEY_COMPARE_HASH_KEY] = self.compare_key
