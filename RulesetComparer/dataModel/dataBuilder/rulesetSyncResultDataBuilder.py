from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties import dataKey as key


class RulesetSyncResultDataBuilder(BaseBuilder):
    def __init__(self, ruleset_sync_pre_json, failed_rulesets_list, created_ruleset_list, updated_ruleset_list, deleted_ruleset_list):
        try:
            self.json_data = ruleset_sync_pre_json
            self.failed_rulesets_list = failed_rulesets_list
            self.created_ruleset_list = created_ruleset_list
            self.updated_ruleset_list = updated_ruleset_list
            self.deleted_ruleset_list = deleted_ruleset_list
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict["country"] = self.json_data[key.COMPARE_RULE_LIST_COUNTRY]
        self.result_dict["source_environment"] = self.json_data["source_environment"]
        self.result_dict["target_environment"] = self.json_data["target_environment"]
        self.result_dict["update_time"] = self.get_current_time()
        self.result_dict["failed_rulesets"] = self.failed_rulesets_list
        self.result_dict["create_rulesets"] = self.created_ruleset_list
        self.result_dict["update_rulesets"] = self.updated_ruleset_list
        self.result_dict["deleted_rulesets"] = self.deleted_ruleset_list
