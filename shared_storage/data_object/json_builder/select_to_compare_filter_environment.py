from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import *


class SelectToCompareFilterEnvironmentBuilder(BaseBuilder):
    def __init__(self, side, environments):
        try:
            self.side = side
            self.environments = environments
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_SIDE] = self.side
        self.result_dict[KEY_TITLE] = "Environment"
        self.result_dict[KEY_TYPE] = "environment"
        self.result_dict[KEY_DATA] = self.environments
