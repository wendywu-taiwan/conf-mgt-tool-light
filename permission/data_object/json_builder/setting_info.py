import RulesetComparer.properties.key as key
from RulesetComparer.date_model.json_builder.base import BaseBuilder
from permission.models import Module, Function
from RulesetComparer.date_model.json_builder.user import UserBuilder
from RulesetComparer.date_model.json_builder.module import ModuleBuilder
from RulesetComparer.date_model.json_builder.function_enable import FunctionEnableBuilder
from RulesetComparer.properties.key import *


class SettingInfoBuilder(BaseBuilder):

    def __init__(self, user):
        self.user = user
        self.module = Module.objects.get(name=KEY_M_SETTING)
        self.function_ids = Function.objects.filter(module=self.module).values_list("id",flat=True)
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_USER_DATA] = UserBuilder(self.user).get_data()
        self.result_dict[KEY_MODULE_DATA] = ModuleBuilder(self.module).get_data()
        self.result_dict[KEY_FUNCTIONS_DATA] = self.parse_functions()

    def parse_functions(self):
        dict = {}
        for function_id in self.function_ids:
            function = Function.objects.get(id=function_id)
            dict[function.name] = FunctionEnableBuilder(self.user.id, function).get_data()
        return dict
