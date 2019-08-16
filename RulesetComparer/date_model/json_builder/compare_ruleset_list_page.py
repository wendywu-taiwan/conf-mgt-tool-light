from RulesetComparer.properties.key import *
from common.data_object.json_builder.base import BaseBuilder


class CompareRulesetListPageBuilder(BaseBuilder):

    def __init__(self, compare_result_data):
        self.compare_result_data = compare_result_data
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict = self.compare_result_data[COMPARE_RESULT_LIST_DATA]
        self.result_dict[KEY_COUNTRY] = self.compare_result_data[KEY_COUNTRY]
        self.result_dict[KEY_BASE_ENV] = self.compare_result_data[KEY_BASE_ENV]
        self.result_dict[KEY_COMPARE_ENV] = self.compare_result_data[KEY_COMPARE_ENV]
