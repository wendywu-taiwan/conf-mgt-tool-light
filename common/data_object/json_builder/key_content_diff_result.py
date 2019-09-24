import traceback
from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import *


class KeyContentDiffResultBuilder(BaseBuilder):
    KEY_LEFT_ONLY = "left_only"
    KEY_RIGHT_ONLY = "right_only"
    KEY_DIFFERENT = "different"
    KEY_COMMON = "common"

    def __init__(self, file_name, left_file_path, right_file_path, left_only_list, right_only_list, different_left_list,
                 common_left_list, right_object_map):
        try:
            self.file_name = file_name
            self.left_file_path = left_file_path
            self.right_file_path = right_file_path
            self.left_only_list = left_only_list
            self.right_only_list = right_only_list
            self.different_left_list = different_left_list
            self.common_left_list = common_left_list
            self.right_object_map = right_object_map
            self.result_list = list()
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
        self.result_dict[KEY_DIFF_RESULT] = self.result_list
        self.result_dict[COMPARE_RESULT_HAS_CHANGES] = self.has_changes

    def parse_left_only_list(self):
        for line_object in self.left_only_list:
            json_object = {
                KEY_TYPE: self.KEY_LEFT_ONLY,
                KEY_LEFT_LINE: line_object.index,
                KEY_LEFT_ROW: line_object.context,
                KEY_RIGHT_LINE: "",
                KEY_RIGHT_ROW: ""
            }
            self.result_list.append(json_object)

    def parse_right_only_list(self):
        for line_object in self.right_only_list:
            json_object = {
                KEY_TYPE: self.KEY_RIGHT_ONLY,
                KEY_LEFT_LINE: "",
                KEY_LEFT_ROW: "",
                KEY_RIGHT_LINE: line_object.index,
                KEY_RIGHT_ROW: line_object.context
            }
            self.result_list.append(json_object)

    def parse_different_list(self):
        for left_object in self.different_left_list:
            right_object = self.right_object_map.get(left_object.key)
            json_object = {
                KEY_TYPE: self.KEY_DIFFERENT,
                KEY_LEFT_LINE: left_object.index,
                KEY_LEFT_ROW: left_object.context,
                KEY_RIGHT_LINE: right_object.index,
                KEY_RIGHT_ROW: right_object.context
            }
            self.result_list.append(json_object)

    def parse_common_list(self):
        for left_object in self.common_left_list:
            right_object = self.right_object_map.get(left_object.key)
            json_object = {
                KEY_TYPE: self.KEY_COMMON,
                KEY_LEFT_LINE: left_object.index,
                KEY_LEFT_ROW: left_object.context,
                KEY_RIGHT_LINE: right_object.index,
                KEY_RIGHT_ROW: right_object.context
            }
            self.result_list.append(json_object)

    def has_different(self):
        if len(self.right_only_list) == 0 and len(self.left_only_list) == 0 and len(self.different_left_list) == 0:
            return False
        else:
            return True
