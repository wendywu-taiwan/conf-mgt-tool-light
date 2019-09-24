from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *


class ContentDiffLineResultBuilder(BaseBuilder):
    KEY_START_SIGN = "\x00"
    KEY_DELETED_SIGN = "\x00-"
    KEY_ADDED_SIGN = "\x00+"
    KEY_END_SIGN = "\x01"
    KEY_CHANGED_SIGN = "\x00^"

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
            self.type = KEY_BLANK
            self.result_list.append(self.build_line_object(KEY_CONTEXT, diff_line_str, 0))
        else:
            self.line = diff_line_index
            if self.KEY_END_SIGN not in diff_line_str:
                self.type = KEY_CONTEXT
                self.result_list.append(self.build_line_object(KEY_CONTEXT, diff_line_str, 0))
            else:
                self.parse_diff_line_sign_object(diff_line_str)

        self.result_list.sort(key=lambda x: x.get(KEY_INDEX), reverse=False)

    def parse_diff_line_sign_object(self, diff_line_str):
        # ex. \x00-# 3 = both\x01
        # split_str_list = ["","# 3 = both\x01"]
        # split_str_list2 = ["# 3 = both",""]

        index = 0
        self.type = KEY_CHANGED
        split_str_list = diff_line_str.split(self.KEY_END_SIGN)

        for string in split_str_list:
            if string is "":
                continue

            if self.KEY_START_SIGN not in string:
                self.result_list.append(self.build_line_object(KEY_CONTEXT, string, index))
            else:
                if self.KEY_ADDED_SIGN in string:
                    split_str_list2 = string.split(self.KEY_ADDED_SIGN)
                elif self.KEY_DELETED_SIGN in string:
                    split_str_list2 = string.split(self.KEY_DELETED_SIGN)
                else:
                    split_str_list2 = string.split(self.KEY_CHANGED_SIGN)

                if split_str_list2[0] is not "":
                    self.result_list.append(self.build_line_object(KEY_CONTEXT, split_str_list2[0], index))
                    index = index + 1

                self.result_list.append(self.build_line_object(KEY_CHANGED, split_str_list2[1], index))

            index = index + 1
        self.result_list.sort(key=lambda x: x.get(KEY_INDEX), reverse=False)

    @staticmethod
    def build_line_object(type, row, index):
        json_object = {
            KEY_TYPE: type,
            KEY_ROW: row,
            KEY_INDEX: index
        }

        return json_object
