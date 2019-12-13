import difflib

from shared_storage.data_object.json_builder.content_diff_result_line_builder import RulesetDiffLineResultBuilder


class StringDiffObject:

    def __init__(self, diff_array):
        self.diff_array = diff_array
        self.left_result = list()
        self.right_result = list()

    def diff(self):
        left_diff = [self.diff_array[0], ""]
        right_diff = [self.diff_array[1], ""]
        diff = difflib._mdiff(left_diff, right_diff)

        diff_list = list(diff)
        diff_data = diff_list[0]
        left_diff_data = diff_data[0]
        right_diff_data = diff_data[1]

        left_row_object = RulesetDiffLineResultBuilder(left_diff_data)
        right_row_object = RulesetDiffLineResultBuilder(right_diff_data)
        self.left_result = left_row_object.get_data()
        self.right_result = right_row_object.get_data()

    def get_left_data(self):
        return self.left_result

    def get_right_data(self):
        return self.right_result
