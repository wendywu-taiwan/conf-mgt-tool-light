import traceback

from RulesetComparer.properties.key import KEY_TYPE, KEY_ROW, KEY_INDEX, KEY_START_SIGN, KEY_DELETED_SIGN, \
    KEY_ADDED_SIGN, KEY_END_SIGN, KEY_CHANGED_SIGN, KEY_CONTEXT, KEY_ADDED, KEY_DELETED, KEY_CHANGED
from RulesetComparer.utils.logger import error_log
from common.data_object.json_builder.base import BaseBuilder


class RulesetDiffResultBuilder(BaseBuilder):
    def __init__(self, diff_list, is_left_data):
        self.index = 0
        self.diff_list = diff_list
        self.is_left_data = is_left_data

        self.result_list = list()
        self.line_data_list = list()
        self.tmp_context = ""
        self.now_type = None
        self.parse_diff_line_result()
        BaseBuilder.__init__(self)

    def parse_diff_line_result(self):
        for diff_data in self.diff_list:
            different = diff_data[2]
            if self.is_left_data:
                diff_tuple = diff_data[0]
            else:
                diff_tuple = diff_data[1]

            context = diff_tuple[1]
            line_index = diff_tuple[0]

            if not isinstance(line_index, int):
                continue

            if not different or KEY_END_SIGN not in context:
                self.add_to_tmp_context(context, KEY_CONTEXT)
            else:
                self.parse_diff_line_sign_object(context)

    def parse_diff_line_sign_object(self, diff_line_str):
        # ex. \x00-# 3 = both\x01
        # split_str_list = ["","# 3 = both\x01"]
        # split_str_list2 = ["# 3 = both",""]

        split_str_list = diff_line_str.split(KEY_END_SIGN)
        if "" in split_str_list:
            split_str_list.remove("")

        for string in split_str_list:
            if KEY_START_SIGN not in string:
                self.add_to_tmp_context(string, KEY_CONTEXT)
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

                if split_str_list2[0] is not "":
                    self.add_to_tmp_context(split_str_list2[0], KEY_CONTEXT)
                try:
                    self.add_to_tmp_context(split_str_list2[1], result_type)
                except IndexError:
                    error_log("index out of range, line text: " + diff_line_str)

        self.result_list.sort(key=lambda x: x.get(KEY_INDEX), reverse=False)

    def add_to_tmp_context(self, context, type):
        if self.now_type is None:
            self.now_type = type

        if type != self.now_type:
            self.add_tmp_context_to_line()

        self.now_type = type
        self.tmp_context = self.tmp_context + context

        if context == ",":
            self.switch_line()

    def add_line_row_data(self, result_type, context):
        self.add_tmp_context_to_line()
        line_index = len(self.line_data_list)
        row_data = self.build_line_object(result_type, context, line_index)
        self.line_data_list.append(row_data)
        if context == ",":
            self.switch_line()

    def switch_line(self):
        try:
            self.add_tmp_context_to_line()
            self.result_list.append(self.build_line_object(KEY_CONTEXT, self.line_data_list, self.index))
            self.index = self.index + 1
            self.line_data_list = list()
        except Exception as e:
            traceback.format_exc()

    def add_tmp_context_to_line(self):
        if self.tmp_context == "":
            return

        line_index = len(self.line_data_list)
        row_data = self.build_line_object(self.now_type, self.tmp_context, line_index)
        self.line_data_list.append(row_data)
        self.tmp_context = ""

    @staticmethod
    def build_line_object(type, row, index):
        json_object = {
            KEY_TYPE: type,
            KEY_ROW: row,
            KEY_INDEX: index
        }

        return json_object

    def __generate_data__(self):
        if len(self.line_data_list) > 0 or self.tmp_context != "":
            self.switch_line()

        self.result_dict = self.result_list
