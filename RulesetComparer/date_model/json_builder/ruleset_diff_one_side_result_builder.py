from RulesetComparer.properties.key import KEY_TYPE, KEY_ROW, KEY_INDEX, KEY_CONTEXT
from common.data_object.json_builder.base import BaseBuilder


class RulesetDiffOneSideResultBuilder(BaseBuilder):
    def __init__(self, context):
        self.context = context
        self.index = 0
        self.line_object_list = list()
        self.result_list = list()
        BaseBuilder.__init__(self)

    @staticmethod
    def build_line_object(type, row, index):
        json_object = {
            KEY_TYPE: type,
            KEY_ROW: row,
            KEY_INDEX: index
        }

        return json_object

    def __generate_data__(self):
        split_str_list = self.context.split(",")
        if "" in split_str_list:
            split_str_list.remove("")

        for string in split_str_list:
            line_object = self.build_line_object(KEY_CONTEXT, string, 0)
            self.line_object_list.append(line_object)
            self.result_list.append(self.build_line_object(KEY_CONTEXT, self.line_object_list, self.index))
            self.line_object_list = list()
            self.index = self.index + 1

        self.result_dict = self.result_list
