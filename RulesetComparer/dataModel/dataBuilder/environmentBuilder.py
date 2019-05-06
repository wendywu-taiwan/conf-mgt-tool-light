from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *


class EnvironmentBuilder(BaseBuilder):
    def __init__(self, environment):
        try:
            self.environment = environment
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.environment.id
        self.result_dict[KEY_NAME] = self.environment.name
        self.result_dict[KEY_FULL_NAME] = self.environment.full_name
