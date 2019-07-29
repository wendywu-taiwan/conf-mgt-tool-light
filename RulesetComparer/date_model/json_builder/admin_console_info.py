import RulesetComparer.properties.key as key
from RulesetComparer.date_model.json_builder.base import BaseBuilder
from permission.models import Module, Function
from RulesetComparer.date_model.json_builder.user import UserBuilder
from RulesetComparer.date_model.json_builder.module import ModuleBuilder
from RulesetComparer.date_model.json_builder.function_enable import FunctionEnableBuilder
from RulesetComparer.properties.key import *


class AdminConsoleInfoBuilder(BaseBuilder):
    DEFAULT_MODULE = "ruleset"

    def __init__(self, user):
        self.user = user
        self.module = Module.objects.get(name=self.DEFAULT_MODULE)
        self.functions = Function.objects.all()
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_USER_DATA] = UserBuilder(self.user).get_data()
        self.result_dict[KEY_MODULE_DATA] = ModuleBuilder(self.module).get_data()
        self.result_dict[KEY_FUNCTIONS_DATA] = self.parse_functions()

    def parse_functions(self):
        dict = {}
        for function in self.functions:
            dict[function.name] = FunctionEnableBuilder(self.user.id, function).get_data()
        return dict
