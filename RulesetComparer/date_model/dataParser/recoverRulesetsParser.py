from RulesetComparer.properties.config import *
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.date_model.dataParser.baseApplyRulesetParser import BaseApplyRulesetParser


class RecoverRulesetsParser(BaseApplyRulesetParser):
    def __init__(self, json_data):
        try:
            self.data = json_data
            BaseApplyRulesetParser.__init__(self)
        except BaseException as e:
            raise e

    def parse_ruleset_data(self):
        self.source_environment = Environment.objects.get(name=BACKUP_ENVIRONMENT_NAME)
        self.target_environment = Environment.objects.get(id=self.data.get(KEY_TARGET_ENV_ID))
        self.country = Country.objects.get(id=self.data[KEY_COUNTRY_ID])
        self.backup_key = self.data[KEY_BACKUP_KEY]
        self.rulesets = self.data[KEY_APPLIED_RULESETS]
        self.ruleset_path = get_backup_path_server_version(self.backup_key)
