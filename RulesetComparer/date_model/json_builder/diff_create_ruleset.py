from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import *


class DiffCreateRulesetBuilder(BaseBuilder):

    def __init__(self, ruleset_name):
        self.ruleset_name = ruleset_name
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_NAME] = self.ruleset_name

    def get_data(self):
        return self.result_dict