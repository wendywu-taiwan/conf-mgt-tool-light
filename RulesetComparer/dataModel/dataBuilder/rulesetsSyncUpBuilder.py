from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties import dataKey as key


class RulesetsSyncUpBuilder(BaseBuilder):
    def __init__(self, json_data):
        try:
            self.json_data = json_data
            self.ruleset_list_json = self.json_data[key.COMPARE_RESULT_LIST_DATA]
            self.ruleset_detail_json = self.json_data[key.COMPARE_RESULT_DETAIL_DATA]
            self.ruleset_diff_json = self.json_data[key.COMPARE_RESULT_DIFF_DATA]
            self.target_environment = None
            self.source_environment = None
            self.parsing_environment()
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def parsing_environment(self):
        base_environment = self.json_data[key.COMPARE_RULE_BASE_ENV]
        compare_environment = self.json_data[key.COMPARE_RULE_COMPARE_ENV]

        self.source_environment = base_environment
        self.target_environment = compare_environment

    def __generate_data__(self):
        self.result_dict["country"] = self.json_data[key.COMPARE_RULE_LIST_COUNTRY]
        self.result_dict["source_environment"] = self.source_environment
        self.result_dict["target_environment"] = self.target_environment
        self.result_dict["compare_time"] = self.ruleset_list_json[key.COMPARE_RESULT_DATE_TIME]
        self.result_dict["compare_hash_key"] = self.ruleset_list_json[key.COMPARE_RULE_COMPARE_HASH_KEY]
        self.result_dict["add_rulesets"] = self.__generate_add_ruleset_list__
        self.result_dict["delete_rulesets"] = self.__generate_delete_ruleset_list__
        self.result_dict["update_rulesets"] = self.__generate_update_ruleset_list__

    def __generate_add_ruleset_list__(self):
        rulesets_list = {}
        rulesets_array = []

        for ruleset in self.ruleset_list_json[key.COMPARE_RESULT_ADD_LIST]:
            ruleset_obj = {"name": ruleset["name"]}
            rulesets_array.append(ruleset_obj)

        rulesets_list["count"] = self.ruleset_list_json[key.COMPARE_RESULT_ADD_FILE_COUNT]
        rulesets_list["rulesets_array"] = rulesets_array
        return rulesets_list

    def __generate_delete_ruleset_list__(self):
        rulesets_list = {}
        rulesets_array = []

        for ruleset in self.ruleset_list_json[key.COMPARE_RESULT_REMOVE_LIST]:
            ruleset_obj = {"name": ruleset["name"]}
            rulesets_array.append(ruleset_obj)

        rulesets_list["count"] = self.ruleset_list_json[key.COMPARE_RESULT_REMOVE_FILE_COUNT]
        rulesets_list["rulesets_array"] = rulesets_array
        return rulesets_list

    def __generate_update_ruleset_list__(self):
        rulesets_list = {}
        rulesets_array = []

        for ruleset in self.ruleset_list_json[key.COMPARE_RESULT_MODIFY_LIST]:
            ruleset_obj = {}

            ruleset_name = ruleset["name"]
            ruleset_diff_obj = self.ruleset_diff_json[ruleset_name]

            ruleset_obj["name"] = ruleset_name
            ruleset_obj["source_env_only_rules"] = self.__generate_rules_obj__(
                ruleset[key.RULE_LIST_ITEM_ADD_COUNT], ruleset_diff_obj[key.RULE_LIST_ITEM_TABLE_TYPE_ADD])
            ruleset_obj["target_env_only_rules"] = self.__generate_rules_obj__(
                ruleset[key.RULE_LIST_ITEM_REMOVE_COUNT], ruleset_diff_obj[key.RULE_LIST_ITEM_TABLE_TYPE_REMOVE])
            ruleset_obj["normal_rules"] = self.__generate_rules_obj__(
                0, ruleset_diff_obj[key.RULE_LIST_ITEM_TABLE_TYPE_NORMAL])
            ruleset_obj["different_rules"] = self.__generate_rules_obj__(
                ruleset[key.RULE_LIST_ITEM_MODIFY_COUNT], ruleset_diff_obj[key.RULE_LIST_ITEM_TABLE_TYPE_MODIFY])
            rulesets_array.append(ruleset_obj)

        rulesets_list["count"] = self.ruleset_list_json[key.COMPARE_RESULT_MODIFY_FILE_COUNT]
        rulesets_list["rulesets_array"] = rulesets_array
        return rulesets_list

    @staticmethod
    def __generate_rules_obj__(ruleset_type_count, ruleset_diff_type_list):
        rules_obj = {}
        rules_array = []
        for rule_detail in ruleset_diff_type_list:
            rule_obj = {"combined_key": rule_detail[key.RULE_KEY_COMBINED_KEY]}
            rules_array.append(rule_obj)

        rules_obj["count"] = ruleset_type_count
        rules_obj["rules_array"] = rules_array
        return rules_obj
