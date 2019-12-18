import difflib

from RulesetComparer.date_model.json_builder.ruleset_diff_result_builder import RulesetDiffResultBuilder
from RulesetComparer.date_model.json_builder.ruleset_diff_one_side_result_builder import RulesetDiffOneSideResultBuilder


class StringDiffObject:

    def __init__(self, diff_array):
        self.diff_array = diff_array
        self.left_result = list()
        self.right_result = list()

    def diff(self):
        left_diff = self.diff_array[0]
        right_diff = self.diff_array[1]

        if left_diff == "":
            self.left_result = ""
            self.right_result = RulesetDiffOneSideResultBuilder(right_diff).get_data()
        elif right_diff == "":
            self.right_result = ""
            self.left_result = RulesetDiffOneSideResultBuilder(left_diff).get_data()
        else:

            diff = difflib._mdiff(left_diff, right_diff)
            diff_list = list(diff)

            left_row_object = RulesetDiffResultBuilder(diff_list, True)
            right_row_object = RulesetDiffResultBuilder(diff_list, False)
            self.left_result = left_row_object.get_data()
            self.right_result = right_row_object.get_data()

    def get_left_data(self):
        return self.left_result

    def get_right_data(self):
        return self.right_result
