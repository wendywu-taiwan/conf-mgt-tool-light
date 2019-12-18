import traceback

from RulesetComparer.utils.logger import error_log
from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.properties.key import KEY_START_SIGN, KEY_DELETED_SIGN, KEY_ADDED_SIGN, KEY_END_SIGN, \
    KEY_CHANGED_SIGN


class ContentDiffLineResultBuilder(BaseBuilder):
    def __init__(self, diff_line_tuple):
        try:
            self.diff_line_tuple = diff_line_tuple
            self.type = None
            self.line = None
            self.result_list = []
            self.parse_diff_line_result()
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.result_list

    def parse_diff_line_result(self):
        diff_line_index = self.diff_line_tuple[0]
        diff_line_str = self.diff_line_tuple[1]

        if not isinstance(diff_line_index, int):
            self.line = ""
            self.type = KEY_CONTEXT
            self.add_to_result_list(KEY_CONTEXT, diff_line_str, 0)

        else:
            self.line = diff_line_index
            if KEY_END_SIGN not in diff_line_str:
                self.type = KEY_CONTEXT
                self.add_to_result_list(KEY_CONTEXT, diff_line_str, 0)
            else:
                self.parse_diff_line_sign_object(diff_line_str)

        self.result_list.sort(key=lambda x: x.get(KEY_INDEX), reverse=False)

    def parse_diff_line_sign_object(self, diff_line_str):
        # ex. \x00-# 3 = both\x01
        # split_str_list = ["","# 3 = both\x01"]
        # split_str_list2 = ["# 3 = both",""]

        index = 0
        split_str_list = diff_line_str.split(KEY_END_SIGN)
        if "" in split_str_list:
            split_str_list.remove("")

        for string in split_str_list:
            if KEY_START_SIGN not in string:
                self.result_list.append(self.build_line_object(KEY_CONTEXT, string, index))
            else:
                if KEY_ADDED_SIGN in string:
                    split_str_list2 = string.split(KEY_ADDED_SIGN)
                    result_type = KEY_ADDED
                elif KEY_DELETED_SIGN in string:
                    split_str_list2 = string.split(KEY_DELETED_SIGN)
                    result_type = KEY_DELETED
                else:
                    split_str_list2 = string.split(KEY_CHANGED_SIGN)
                    result_type = KEY_CHANGED

                self.type = result_type
                if split_str_list2[0] is not "":
                    index = index + 1
                    self.result_list.append(self.build_line_object(KEY_CONTEXT, split_str_list2[0], index))
                try:
                    self.result_list.append(self.build_line_object(result_type, split_str_list2[1], index))
                except IndexError:
                    error_log("index out of range, line text: " + diff_line_str)

            index = index + 1
        self.result_list.sort(key=lambda x: x.get(KEY_INDEX), reverse=False)
        if len(self.result_list) > 1:
            self.type = KEY_CHANGED

    def add_to_result_list(self, result_type, value, index):
        self.result_list.append(self.build_line_object(result_type, value, index))

    @staticmethod
    def build_line_object(type, row, index):
        json_object = {
            KEY_TYPE: type,
            KEY_ROW: row,
            KEY_INDEX: index
        }

        return json_object