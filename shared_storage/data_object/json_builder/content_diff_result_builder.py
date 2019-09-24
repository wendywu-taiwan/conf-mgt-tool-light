import traceback
from common.data_object.json_builder.base import BaseBuilder
from shared_storage.data_object.json_builder.content_diff_result_line_builder import ContentDiffLineResultBuilder
from RulesetComparer.properties.config import *


class ContentDiffResultBuilder(BaseBuilder):
    def __init__(self, file_name, left_file, right_file, diff_list):
        try:
            self.file_name = file_name
            self.left_file = left_file
            self.right_file = right_file
            self.diff_list = diff_list
            self.has_different = False
            BaseBuilder.__init__(self)
        except Exception as e:
            traceback.print_exc()
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_FILE_NAME] = self.file_name
        self.result_dict[KEY_LEFT_FILE] = self.left_file
        self.result_dict[KEY_RIGHT_FILE] = self.right_file
        self.result_dict[KEY_DIFF_RESULT] = self.parse_diff_result()
        self.result_dict[COMPARE_RESULT_HAS_CHANGES] = self.has_different

    def parse_diff_result(self):
        diff_result = []
        for line in self.diff_list:
            left_diff_result = line[0]
            right_diff_result = line[1]
            if line[2] is True:
                self.has_different = True

            row_json = {}
            left_row_object = ContentDiffLineResultBuilder(left_diff_result)
            right_row_object = ContentDiffLineResultBuilder(right_diff_result)
            row_json[KEY_LEFT_TYPE] = left_row_object.type
            row_json[KEY_LEFT_LINE] = left_row_object.line
            row_json[KEY_LEFT_ROW] = left_row_object.get_data()
            row_json[KEY_RIGHT_TYPE] = right_row_object.type
            row_json[KEY_RIGHT_LINE] = right_row_object.line
            row_json[KEY_RIGHT_ROW] = right_row_object.get_data()

            diff_result.append(row_json)
        return diff_result
