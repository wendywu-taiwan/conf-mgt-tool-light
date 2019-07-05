from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.dataKey import *
from RulesetComparer.dataModel.dataBuilder.environmentBuilder import EnvironmentBuilder
from RulesetComparer.dataModel.dataBuilder.countryBuilder import CountryBuilder


class RecoverRulesetsResultBuilder(BaseBuilder):
    def __init__(self, target_env, country, sync_result_obj):
        try:
            self.target_env = target_env
            self.country = country
            self.failed_rulesets_list = sync_result_obj.failed_list
            self.created_ruleset_list = sync_result_obj.created_list
            self.updated_ruleset_list = sync_result_obj.updated_list
            self.deleted_ruleset_list = sync_result_obj.delete_list
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_TARGET_ENV] = EnvironmentBuilder(environment=self.target_env).get_data()
        self.result_dict[KEY_COUNTRY] = CountryBuilder(self.country).get_data()
        self.result_dict[KEY_UPDATED_TIME] = self.get_current_time()
        self.result_dict[KEY_FAILED_RULESETS] = self.failed_rulesets_list
        self.result_dict[KEY_CREATED_RULESETS] = self.created_ruleset_list
        self.result_dict[KEY_UPDATED_RULESETS] = self.updated_ruleset_list
        self.result_dict[KEY_DELETED_RULESETS] = self.deleted_ruleset_list
