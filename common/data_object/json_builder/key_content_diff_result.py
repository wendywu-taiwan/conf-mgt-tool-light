import traceback
from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import *


class KeyContentDiffResultBuilder(BaseBuilder):
    KEY_LEFT_ONLY = "left_only"
    KEY_RIGHT_ONLY = "right_only"
    KEY_DIFFERENT = "different"
    KEY_COMMON = "common"

    def __init__(self, file_name, left_file_path, right_file_path, left_modification_time, right_modification_time,
                 left_only_list, right_only_list, different_left_list, common_left_list, right_object_map):
        try:
            self.file_name = file_name
            self.left_file_path = left_file_path
            self.right_file_path = right_file_path
            self.left_modification_time = left_modification_time
            self.right_modification_time = right_modification_time
            self.left_only_list = left_only_list
            self.right_only_list = right_only_list
            self.different_left_list = different_left_list
            self.common_left_list = common_left_list
            self.right_object_map = right_object_map
            self.has_changes = False
            super().__init__()
        except Exception as e:
            traceback.print_exc()
            raise e

    def __generate_data__(self):
        self.parse_left_only_list()
        self.parse_right_only_list()
        self.parse_different_list()
        self.parse_common_list()
        self.has_changes = self.has_different()

        self.result_dict[KEY_FILE_NAME] = self.file_name
        self.result_dict[KEY_LEFT_FILE] = self.left_file_path
        self.result_dict[KEY_RIGHT_FILE] = self.right_file_path
        self.result_dict[KEY_LEFT_MODIFICATION_TIME] = self.left_modification_time
        self.result_dict[KEY_RIGHT_MODIFICATION_TIME] = self.right_modification_time
        self.result_dict[KEY_DIFF_RESULT] = self.parse_diff_result_object()
        self.result_dict[COMPARE_RESULT_HAS_CHANGES] = self.has_changes

    def parse_diff_result_object(self):
        diff_result_object = {
            KEY_LEFT_ONLY: self.parse_left_only_list(),
            KEY_RIGHT_ONLY: self.parse_right_only_list(),
            KEY_COMMON: self.parse_common_list(),
            KEY_DIFFERENT: self.parse_different_list()
        }
        return diff_result_object

    def parse_left_only_list(self):
        result_list = list()
        for line_object in self.left_only_list:
            json_object = {
                KEY_TYPE: self.KEY_LEFT_ONLY,
                KEY_LEFT_LINE: line_object.index,
                KEY_LEFT_ROW: line_object.context,
                KEY_RIGHT_LINE: "",
                KEY_RIGHT_ROW: ""
            }
            result_list.append(json_object)
        return result_list

    def parse_right_only_list(self):
        result_list = list()

        for line_object in self.right_only_list:
            json_object = {
                KEY_TYPE: self.KEY_RIGHT_ONLY,
                KEY_LEFT_LINE: "",
                KEY_LEFT_ROW: "",
                KEY_RIGHT_LINE: line_object.index,
                KEY_RIGHT_ROW: line_object.context
            }
            result_list.append(json_object)
        return result_list

    def parse_different_list(self):
        result_list = list()
        for left_object in self.different_left_list:
            right_object = self.right_object_map.get(left_object.key)
            json_object = {
                KEY_TYPE: self.KEY_DIFFERENT,
                KEY_LEFT_LINE: left_object.index,
                KEY_LEFT_ROW: left_object.context,
                KEY_RIGHT_LINE: right_object.index,
                KEY_RIGHT_ROW: right_object.context
            }
            result_list.append(json_object)
        return result_list

    def parse_common_list(self):
        result_list = list()
        for left_object in self.common_left_list:
            right_object = self.right_object_map.get(left_object.key)
            json_object = {
                KEY_TYPE: self.KEY_COMMON,
                KEY_LEFT_LINE: left_object.index,
                KEY_LEFT_ROW: left_object.context,
                KEY_RIGHT_LINE: right_object.index,
                KEY_RIGHT_ROW: right_object.context
            }
            result_list.append(json_object)
        return result_list

    def has_different(self):
        if len(self.right_only_list) == 0 and len(self.left_only_list) == 0 and len(self.different_left_list) == 0:
            return False
        else:
            return True
