from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *


class ModuleBuilder(BaseBuilder):
    def __init__(self, module):
        try:
            self.module = module
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.module.id
        self.result_dict[KEY_NAME] = self.module.name
        self.result_dict[KEY_DISPLAY_NAME] = self.module.display_name
