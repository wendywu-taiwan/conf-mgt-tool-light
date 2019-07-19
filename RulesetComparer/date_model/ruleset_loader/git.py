from RulesetComparer.date_model.ruleset_loader.base import BaseRulesetLoader
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.models import Country


class GitRulesetLoader(BaseRulesetLoader):
    def __init__(self, country_id, ruleset_name, check_update):
        try:
            BaseRulesetLoader.__init__(self)
            self.environment = Environment.objects.get(name=GIT.get("environment_name"))
            self.country = Country.objects.get(id=country_id)
            self.ruleset_name = ruleset_name
            self.check_update = check_update
            self.__check_update__()
            BaseRulesetLoader.__load_ruleset__(self)
        except Exception as e:
            raise e

    def __check_update__(self):
        if self.check_update:
            manager = GitManager(get_ruleset_git_root_path(), settings.GIT_BRANCH_DEVELOP)
            manager.pull()

    def __parse_ruleset_path__(self):
        self.ruleset_path = get_rule_set_git_path(self.country.name)

    def __parse_ruleset_path_info__(self):
        pass
