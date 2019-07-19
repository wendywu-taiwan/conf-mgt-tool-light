from RulesetComparer.date_model.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties import dataKey as key


class RulesetSyncResultDataBuilder(BaseBuilder):
    def __init__(self, ruleset_sync_pre_json, sync_result_obj):
        try:
            self.json_data = ruleset_sync_pre_json
            self.failed_rulesets_list = sync_result_obj.failed_list
            self.created_ruleset_list = sync_result_obj.created_list
            self.updated_ruleset_list = sync_result_obj.updated_list
            self.deleted_ruleset_list = sync_result_obj.delete_list
            self.updated_ruleset = False
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

        if len(self.failed_rulesets_list) > 0 or len(self.created_ruleset_list) > 0 or len(
                self.updated_ruleset_list) > 0 or len(self.deleted_ruleset_list) > 0:
            self.updated_ruleset = True
