from RulesetComparer.properties.key import *
from common.data_object.json_builder.navigation_info import NavigationInfoBuilder


class AdminConsoleInfoBuilder(NavigationInfoBuilder):

    def __init__(self, user):
        self.user = user
        if user is None:
            return

        NavigationInfoBuilder.__init__(self, user, KEY_M_RULESET)

    def __generate_data__(self):
        super().__generate_data__()

    def parse_modules(self):
        return super().parse_modules()

    def parse_functions(self):
        return super().parse_functions()
