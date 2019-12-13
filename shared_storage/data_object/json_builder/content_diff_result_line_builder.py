import traceback

from RulesetComparer.utils.logger import error_log
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
            self.type = KEY_CONTEXT
            self.add_to_result_list(KEY_CONTEXT, diff_line_str, 0)

        else:
            self.line = diff_line_index
            if self.KEY_END_SIGN not in diff_line_str:
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
        split_str_list = diff_line_str.split(self.KEY_END_SIGN)
        if "" in split_str_list:
            split_str_list.remove("")

        for string in split_str_list:
            if self.KEY_START_SIGN not in string:
                self.result_list.append(self.build_line_object(KEY_CONTEXT, string, index))
            else:
                if self.KEY_ADDED_SIGN in string:
                    split_str_list2 = string.split(self.KEY_ADDED_SIGN)
                    result_type = KEY_ADDED
                elif self.KEY_DELETED_SIGN in string:
                    split_str_list2 = string.split(self.KEY_DELETED_SIGN)
                    result_type = KEY_DELETED
                else:
                    split_str_list2 = string.split(self.KEY_CHANGED_SIGN)
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


class RulesetDiffLineResultBuilder(ContentDiffLineResultBuilder):
    def __init__(self, diff_line_tuple):
        self.index = 0
        self.line_data_list = list()
        ContentDiffLineResultBuilder.__init__(self, diff_line_tuple)

    def parse_diff_line_sign_object(self, diff_line_str):
        # ex. \x00-# 3 = both\x01
        # split_str_list = ["","# 3 = both\x01"]
        # split_str_list2 = ["# 3 = both",""]

        split_str_list = diff_line_str.split(self.KEY_END_SIGN)
        if "" in split_str_list:
            split_str_list.remove("")

        for string in split_str_list:
            if self.KEY_START_SIGN not in string:
                self.add_to_result_list(KEY_CONTEXT, string, self.index)
            else:
                if self.KEY_ADDED_SIGN in string:
                    split_str_list2 = string.split(self.KEY_ADDED_SIGN)
                    result_type = KEY_ADDED
                elif self.KEY_DELETED_SIGN in string:
                    split_str_list2 = string.split(self.KEY_DELETED_SIGN)
                    result_type = KEY_DELETED
                else:
                    split_str_list2 = string.split(self.KEY_CHANGED_SIGN)
                    result_type = KEY_CHANGED

                self.type = result_type
                if split_str_list2[0] is not "":
                    self.add_to_result_list(KEY_CONTEXT, split_str_list2[0], self.index)
                try:
                    self.add_to_result_list(result_type, split_str_list2[1], self.index)
                except IndexError:
                    error_log("index out of range, line text: " + diff_line_str)

        self.result_list.sort(key=lambda x: x.get(KEY_INDEX), reverse=False)
        if len(self.result_list) > 1:
            self.type = KEY_CHANGED

    def add_to_result_list(self, result_type, value, index):
        if ',' not in value:
            self.add_line_row_data(result_type, value)
        else:
            split_array = value.split(",")
            last_text = split_array[-1]

            for text in split_array:
                if text == last_text and last_text == "":
                    continue
                else:
                    self.add_line_row_data(result_type, text)

                    if text == last_text and last_text != "":
                        continue

                    self.switch_line()

    def add_line_row_data(self, result_type, text):
        line_data_list = self.line_data_list
        if line_data_list is None:
            line_data_list = list()

        line_index = len(line_data_list) + 1
        row_data = self.build_line_object(result_type, text, line_index)
        line_data_list.append(row_data)
        self.line_data_list = line_data_list

    def switch_line(self):
        try:
            line_data_list = self.line_data_list
            if line_data_list is None:
                line_data_list = list()

            self.result_list.append(self.build_line_object(KEY_CONTEXT, line_data_list, self.index))
            self.index = self.index + 1
            self.line_data_list = list()
        except Exception as e:
            traceback.format_exc()

    def __generate_data__(self):
        if len(self.line_data_list) > 0:
            self.switch_line()

        self.result_dict = self.result_list
