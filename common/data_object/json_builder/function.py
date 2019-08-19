from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from permission.models import Function
from permission.utils.permission_manager import check_function_enable


class FunctionBuilder(BaseBuilder):

    def __init__(self, id=None, function=None):
        try:
            if id is None:
                self.function = function
            else:
                self.function = Function.objects.get(id=id)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.function.id
        self.result_dict[KEY_NAME] = self.function.name


class FunctionSBuilder(BaseBuilder):

    def __init__(self, ids=None, functions=None):
        try:
            self.functions = []
            if ids is None:
                self.functions = functions
            else:
                for id in ids:
                    self.functions.append(Function.objects.get(id=id))
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.parse_environments()

    def parse_environments(self):
        array = []
        for function in self.functions:
            data = FunctionBuilder(function=function).get_data()
            array.append(data)
        return array


class FunctionEnableBuilder(BaseBuilder):
    def __init__(self, user_id, function):
        try:
            self.user_id = user_id
            self.function = function
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.function.id
        self.result_dict[KEY_NAME] = self.function.name
        self.result_dict[KEY_VISIBLE] = check_function_enable(self.user_id, self.function.id)
