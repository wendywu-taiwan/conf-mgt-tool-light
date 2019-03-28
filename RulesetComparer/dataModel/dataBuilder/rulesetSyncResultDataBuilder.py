from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties import dataKey as key


class RulesetSyncPreDataBuilder(BaseBuilder):
    def __init__(self, ruleset_sync_pre_json, created_ruleset_list, updated_ruleset_list, deleted_ruleset_list):
        try:
            self.json_data = ruleset_sync_pre_json
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
        self.result_dict["create_rules"] = self.created_ruleset_list
        self.result_dict["update_rules"] = self.updated_ruleset_list
        self.result_dict["deleted_rules"] = self.deleted_ruleset_list
