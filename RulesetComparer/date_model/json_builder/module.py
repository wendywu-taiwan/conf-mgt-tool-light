from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from permission.models import RoleFunctionPermission, Function


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


class ModuleVisibleBuilder(ModuleBuilder):
    def __init__(self, module, user):
        try:
            self.module = module
            self.user = user
            ModuleBuilder.__init__(self, module)
        except Exception as e:
            raise e

    def __generate_data__(self):
        super().__generate_data__()
        self.result_dict[KEY_VISIBLE] = self.parse_visibility()

    def parse_visibility(self):
        function_ids = Function.objects.filter(module=self.module).values_list("id", flat=True)
        visible_count = RoleFunctionPermission.objects.filter(function_id__in=function_ids,
                                                              role_permission__user_role_permission_role_permission__user=self.user,
                                                              visible=1).count()
        if visible_count > 0:
            return 1
        else:
            return 0
