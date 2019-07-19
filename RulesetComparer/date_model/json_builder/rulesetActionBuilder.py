from RulesetComparer.date_model.json_builder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *


class RulesetActionBuilder(BaseBuilder):
    def __init__(self, action):
        try:
            self.action = action
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.action.id
        self.result_dict[KEY_NAME] = self.action.name
        self.result_dict[KEY_CAPITAL_NAME] = self.action.capital_name
