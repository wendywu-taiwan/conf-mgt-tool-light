import RulesetComparer.properties.dataKey as key
from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder


class CompareReportInfoBuilder(BaseBuilder):

    def __init__(self):
        self.data_list = list()
        BaseBuilder.__init__(self)

    def clear_data(self):
        self.data_list.clear()
        self.result_dict.clear()

    def add_data(self, result_data):
        list_data = result_data[key.COMPARE_RESULT_LIST_DATA]
        list_data[key.COMPARE_RULE_LIST_COUNTRY] = result_data[key.COMPARE_RULE_LIST_COUNTRY]

        self.result_dict[key.COMPARE_RULE_BASE_ENV] = result_data[key.COMPARE_RULE_BASE_ENV]
        self.result_dict[key.COMPARE_RULE_COMPARE_ENV] = result_data[key.COMPARE_RULE_COMPARE_ENV]
        self.result_dict[key.COMPARE_RESULT_DATE_TIME] = list_data[key.COMPARE_RESULT_DATE_TIME]

        self.data_list.append(list_data)

    def __generate_data__(self):
        pass

    def get_data(self):
        self.result_dict[key.COMPARE_RESULT_INFO_DATA] = self.data_list
        return self.result_dict
