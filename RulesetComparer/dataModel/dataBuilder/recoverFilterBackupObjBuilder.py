from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.utils.stringFilter import *


class RecoverFilterBackupObjBuilder(BaseBuilder):
    def __init__(self, pre_json, update_time, backup_key, filter_keys):
        try:
            self.json_data = pre_json
            self.filter_keys = filter_keys
            self.update_time = update_time
            self.backup_key = backup_key
            self.source_env_only_rulesets = pre_json.get(KEY_SOURCE_ENV_ONLY_RULESETS)
            self.target_env_only_rulesets = pre_json.get(KEY_TARGET_ENV_ONLY_RULESETS)
            self.different_rulesets = pre_json.get(KEY_DIFFERENT_RULESETS)
            self.has_filtered_rulesets = False
            self.log_count = 0
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        # self.result_dict[KEY_CREATED_RULESETS] = self.__generate_rulesets_object__(self.source_env_only_rulesets)
        self.result_dict[KEY_UPDATE_TIME] = self.update_time
        self.result_dict[KEY_BACKUP_KEY] = self.backup_key
        self.result_dict[KEY_CREATED_RULESETS] = self.__generate_no_rulesets_object__()
        self.result_dict[KEY_UPDATED_RULESETS] = self.__generate_rulesets_object__(self.different_rulesets)
        self.result_dict[KEY_DELETED_RULESETS] = self.__generate_no_rulesets_object__()
        # self.result_dict[KEY_DELETED_RULESETS] = self.__generate_rulesets_object__(self.target_env_only_rulesets)

    def __generate_rulesets_object__(self, rulesets):
        rulesets_object = {}
        rulesets_array = []

        for ruleset_obj in rulesets.get(KEY_RULESETS_ARRAY):
            ruleset_name = ruleset_obj.get(KEY_NAME)
            if len(self.filter_keys) == 0:
                rulesets_array.append(ruleset_name)
                self.has_filtered_rulesets = True
            else:
                match = string_filter(ruleset_name, self.filter_keys)
                if match:
                    rulesets_array.append(ruleset_name)
                    self.has_filtered_rulesets = True

        rulesets_object[KEY_COUNT] = len(rulesets_array)
        rulesets_object[KEY_RULESETS_ARRAY] = rulesets_array
        self.log_count += len(rulesets_array)
        return rulesets_object

    @staticmethod
    def __generate_no_rulesets_object__():
        rulesets_object = {}
        rulesets_array = []

        rulesets_object[KEY_COUNT] = len(rulesets_array)
        rulesets_object[KEY_RULESETS_ARRAY] = rulesets_array

        return rulesets_object
