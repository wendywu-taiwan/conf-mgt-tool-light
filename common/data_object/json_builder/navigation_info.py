from common.data_object.json_builder.base import BaseBuilder
from common.data_object.json_builder.function import FunctionEnableBuilder
from common.data_object.json_builder.user import UserBuilder
from common.data_object.json_builder.module import ModuleBuilder, ModuleVisibleBuilder
from permission.models import Module, Function
from RulesetComparer.properties.key import *


class NavigationInfoBuilder(BaseBuilder):

    def __init__(self, user, module_name):
        self.user = user
        self.module = Module.objects.get(name=module_name)
        self.function_ids = Function.objects.filter(module=self.module).values_list("id", flat=True)
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_USER_DATA] = UserBuilder(self.user).get_data()
        self.result_dict[KEY_MODULE_DATA] = self.parse_modules()
        self.result_dict[KEY_FUNCTIONS_DATA] = self.parse_functions()

    def parse_modules(self):
        dict = {}
        module_ids = Module.objects.exclude(id=self.module.id).values_list("id", flat=True)

        for module_id in module_ids:
            module = Module.objects.get(id=module_id)
            dict[module.name] = ModuleVisibleBuilder(module, self.user).get_data()

        dict["current_module"] = ModuleBuilder(self.module).get_data()
        return dict

    def parse_functions(self):
        dict = {}
        for function_id in self.function_ids:
            function = Function.objects.get(id=function_id)
            dict[function.name] = FunctionEnableBuilder(self.user.id, function).get_data()
        return dict
