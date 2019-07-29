from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from permission.utils.permission_manager import check_function_enable


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
