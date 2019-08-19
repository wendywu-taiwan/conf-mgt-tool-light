from common.data_object.json_builder.navigation_info import NavigationInfoBuilder
from RulesetComparer.properties.key import *


class SettingInfoBuilder(NavigationInfoBuilder):

    def __init__(self, user):
        self.user = user
        NavigationInfoBuilder.__init__(self, self.user, KEY_M_SETTING)

    def __generate_data__(self):
        super().__generate_data__()

    def parse_modules(self):
        return super().parse_modules()

    def parse_functions(self):
        return super().parse_functions()
