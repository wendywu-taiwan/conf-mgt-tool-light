from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.dataKey import *


class RecoverRulesetsResultBuilder(BaseBuilder):
    def __init__(self, environment, country, failed_rulesets_list, created_ruleset_list, updated_ruleset_list, deleted_ruleset_list):
        try:
            self.environment = environment
            self.country = country
            self.failed_rulesets_list = failed_rulesets_list
            self.created_ruleset_list = created_ruleset_list
            self.updated_ruleset_list = updated_ruleset_list
            self.deleted_ruleset_list = deleted_ruleset_list
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENT] = self.environment
        self.result_dict[KEY_COUNTRY] = self.country
        self.result_dict[KEY_UPDATED_TIME] = self.get_current_time()
        self.result_dict[KEY_FAILED_RULESETS] = self.failed_rulesets_list
        self.result_dict[KEY_CREATED_RULESETS] = self.created_ruleset_list
        self.result_dict[KEY_UPDATED_RULESETS] = self.updated_ruleset_list
        self.result_dict[KEY_DELETED_RULESETS] = self.deleted_ruleset_list
