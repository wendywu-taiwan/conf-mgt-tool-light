from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.utils.timeUtil import time_change_format
from RulesetComparer.utils.stringFilter import *


class RecoverFilterBackupObjBuilder(BaseBuilder):
    def __init__(self, date_folder_name, pre_json, filter_keys):
        try:
            self.date_folder_name = date_folder_name
            self.json_data = pre_json
            self.filter_keys = filter_keys
            self.has_filter_keys = False
            self.source_env_only_rulesets = pre_json.get(KEY_SOURCE_ENV_ONLY_RULESETS)
            self.target_env_only_rulesets = pre_json.get(KEY_TARGET_ENV_ONLY_RULESETS)
            self.different_rulesets = pre_json.get(KEY_DIFFERENT_RULESETS)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_FOLDER_NAME] = self.date_folder_name
        self.result_dict[KEY_DATE_TIME] = self.__parse_date_time__()
        self.result_dict[KEY_CREATED_RULESETS] = self.__generate_rulesets_object__(self.source_env_only_rulesets)
        self.result_dict[KEY_UPDATED_RULESETS] = self.__generate_rulesets_object__(self.different_rulesets)
        self.result_dict[KEY_DELETED_RULESETS] = self.__generate_rulesets_object__(self.target_env_only_rulesets)
        self.has_filter_keys = self.__has_filtered_keys__()

    def __generate_rulesets_object__(self, rulesets):
        rulesets_object = {}
        rulesets_array = []

        for ruleset_obj in rulesets.get(KEY_RULESETS_ARRAY):
            ruleset_name = ruleset_obj.get(KEY_NAME)
            if len(self.filter_keys) == 0:
                rulesets_array.append(ruleset_name)
            else:
                match = string_filter(ruleset_name, self.filter_keys)
                if match:
                    rulesets_array.append(ruleset_name)

        rulesets_object[KEY_COUNT] = len(rulesets_array)
        rulesets_object[KEY_RULESETS_ARRAY] = rulesets_array

        return rulesets_object

    def __parse_date_time__(self):
        origin_format = TIME_FORMAT.get("time_format_without_slash")
        new_format = TIME_FORMAT.get("year_month_date_hour_minute_second")
        date_time = time_change_format(self.date_folder_name, origin_format, new_format)
        return date_time

    def __has_filtered_keys__(self):
        if len(self.result_dict[KEY_CREATED_RULESETS]) == 0 and \
                len(self.result_dict[KEY_UPDATED_RULESETS]) == 0 and \
                len(self.result_dict[KEY_DELETED_RULESETS]) == 0:
            return False
        else:
            return True
