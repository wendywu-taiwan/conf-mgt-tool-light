from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from common.models import FrequencyType


class FrequencyTypeBuilder(BaseBuilder):
    def __init__(self, frequency_type):
        try:
            self.frequency_type = frequency_type
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.frequency_type.id
        self.result_dict[KEY_DISPLAY_NAME] = self.frequency_type.display_name


class FrequencyTypesBuilder(BaseBuilder):
    def __init__(self, frequency_types):
        try:
            self.frequency_types = frequency_types
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.parse_frequency_data()

    def parse_frequency_data(self):
        array = []
        for frequency_type in self.frequency_types:
            data = FrequencyTypeBuilder(frequency_type).get_data()
            array.append(data)
        return array
