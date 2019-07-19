import RulesetComparer.properties.dataKey as key
from RulesetComparer.date_model.json_builder.baseBuilder import BaseBuilder
from RulesetComparer.properties import config


class CompareReportInfoBuilder(BaseBuilder):

    def __init__(self, json_data, mail_content_type_list):
        try:
            self.json_data = json_data
            self.ruleset_list_json = self.json_data[key.COMPARE_RESULT_LIST_DATA]
            self.normal_environment = None
            self.developer_environment = None
            self.normal_is_base_env = False
            self.show_ruleset_list = False
            self.show_ruleset_table = False
            self.parsing_environment()
            self.parsing_mail_content_type(mail_content_type_list)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def parsing_environment(self):
        base_environment = self.json_data[key.COMPARE_RULE_BASE_ENV]
        compare_environment = self.json_data[key.COMPARE_RULE_COMPARE_ENV]

        if base_environment["name"] == config.GIT.get("environment_name") \
                or compare_environment["name"] == "PROD":
            self.developer_environment = base_environment
            self.normal_environment = compare_environment
            self.normal_is_base_env = False
        elif compare_environment["name"] == config.GIT.get("environment_name") \
                or base_environment["name"] == "PROD":
            self.developer_environment = compare_environment
            self.normal_environment = base_environment
            self.normal_is_base_env = True
        else:
            self.normal_environment = base_environment
            self.developer_environment = compare_environment
            self.normal_is_base_env = True

    def parsing_mail_content_type(self, mail_content_type_list):
        for mail_content_type_obj in mail_content_type_list:
            if mail_content_type_obj.name == key.RULESET_COUNT_TABLE:
                self.show_ruleset_table = True
            elif mail_content_type_obj.name == key.RULESET_NAME_LIST:
                self.show_ruleset_list = True

    def clear_data(self):
        self.result_dict.clear()

    def __generate_data__(self):
        self.result_dict["country"] = self.json_data[key.COMPARE_RULE_LIST_COUNTRY]
        self.result_dict["normal_environment"] = self.normal_environment
        self.result_dict["developer_environment"] = self.developer_environment
        self.result_dict["compare_time"] = self.ruleset_list_json[key.COMPARE_RESULT_DATE_TIME]
        self.result_dict["compare_hash_key"] = self.ruleset_list_json[key.COMPARE_RULE_COMPARE_HASH_KEY]
        self.result_dict["diff_table"] = self.__generate_diff_table__()
        self.result_dict["ruleset_list"] = self.__generate_ruleset_list__()
        self.result_dict["has_changes"] = self.ruleset_list_json[key.COMPARE_RESULT_HAS_CHANGES]

    def __generate_diff_table__(self):
        diff_table = {"different_rulesets_count": self.ruleset_list_json[key.COMPARE_RESULT_MODIFY_FILE_COUNT],
                      "different_rules_count": self.ruleset_list_json[key.COMPARE_RESULT_MODIFY_RULE_COUNT]}

        if self.show_ruleset_table:
            diff_table["show"] = "true"
        else:
            diff_table["show"] = "false"

        if self.normal_is_base_env:
            diff_table["normal_env_only_rulesets_count"] = self.ruleset_list_json[key.COMPARE_RESULT_REMOVE_FILE_COUNT]
            diff_table["developer_env_only_rulesets_count"] = self.ruleset_list_json[key.COMPARE_RESULT_ADD_FILE_COUNT]
            diff_table["normal_env_only_rules_count"] = self.ruleset_list_json[key.COMPARE_RESULT_REMOVE_RULE_COUNT]
            diff_table["developer_env_only_rules_count"] = self.ruleset_list_json[key.COMPARE_RESULT_ADD_RULE_COUNT]
        else:
            diff_table["normal_env_only_rulesets_count"] = self.ruleset_list_json[key.COMPARE_RESULT_ADD_FILE_COUNT]
            diff_table["developer_env_only_rulesets_count"] = self.ruleset_list_json[
                key.COMPARE_RESULT_REMOVE_FILE_COUNT]
            diff_table["normal_env_only_rules_count"] = self.ruleset_list_json[key.COMPARE_RESULT_ADD_RULE_COUNT]
            diff_table["developer_env_only_rules_count"] = self.ruleset_list_json[key.COMPARE_RESULT_REMOVE_RULE_COUNT]
        return diff_table

    def __generate_ruleset_list__(self):
        different_rulesets = self.ruleset_list_json[key.COMPARE_RESULT_MODIFY_LIST]
        if self.normal_is_base_env:
            normal_env_only_rulesets = self.ruleset_list_json[key.COMPARE_RESULT_REMOVE_LIST]
            developer_env_only_rulesets = self.ruleset_list_json[key.COMPARE_RESULT_ADD_LIST]
        else:
            normal_env_only_rulesets = self.ruleset_list_json[key.COMPARE_RESULT_ADD_LIST]
            developer_env_only_rulesets = self.ruleset_list_json[key.COMPARE_RESULT_REMOVE_LIST]

        ruleset_list = {"normal_env_only_rulesets": normal_env_only_rulesets,
                        "developer_env_only_rulesets": developer_env_only_rulesets,
                        "different_rulesets": different_rulesets}

        if self.show_ruleset_list:
            ruleset_list["show"] = "true"
        else:
            ruleset_list["show"] = "false"

        return ruleset_list

    def get_data(self):
        return self.result_dict
