import RulesetComparer.properties.dataKey as key
from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.models import UserRole, Module
from RulesetComparer.serializers.serializers import UserRoleSerializer, ModuleSerializer


class AdminConsoleInfoBuilder(BaseBuilder):
    DEFAULT_USER_ROLE = "Admin"
    DEFAULT_MODULE = "Ruleset"

    def __init__(self, user_role_id=None, module_id=None):
        if user_role_id is None:
            self.user_role = UserRole.objects.get(name=self.DEFAULT_USER_ROLE)
        else:
            self.user_role = UserRole.objects.get(id=user_role_id)

        if module_id is None:
            self.module = Module.objects.get(name=self.DEFAULT_MODULE)
        else:
            self.module = Module.objects.get(id=module_id)

        BaseBuilder.__init__(self)

    def __generate_data__(self):
        user_role_data = UserRoleSerializer(self.user_role).data
        module_data = ModuleSerializer(self.module).data

        self.result_dict = {
            "user_role": user_role_data,
            "module": module_data
        }
