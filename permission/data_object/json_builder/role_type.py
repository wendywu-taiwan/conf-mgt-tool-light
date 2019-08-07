from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import *


class RoleTypeBuilder(BaseBuilder):

    def __init__(self, role_type):
        self.role_type = role_type
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.role_type.id
        self.result_dict[KEY_NAME] = self.role_type.name
        self.result_dict[KEY_DISPLAY_NAME] = self.role_type.display_name
