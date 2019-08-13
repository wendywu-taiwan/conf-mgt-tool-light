import traceback
from RulesetComparer.utils.logger import error_log
from permission.data_object.json_builder.base import SettingBaseBuilder
from permission.models import RolePermission, Environment, RoleType, Function, RoleFunctionPermission
from permission.data_object.json_builder.role_type import RoleTypeBuilder
from RulesetComparer.date_model.json_builder.environment import EnvironmentBuilder
from RulesetComparer.date_model.json_builder.function import FunctionBuilder
from RulesetComparer.properties.key import *


class RolePermissionBuilder(SettingBaseBuilder):
    DISABLE = 0

    def __init__(self, user):
        try:
            self.environment_ids = Environment.objects.all().values_list("id", flat=True)
            SettingBaseBuilder.__init__(self, user)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict["data"] = self.parse_role_permission_objects()

    def parse_role_permission_objects(self):
        try:
            data_array = []
            for environment_id in self.environment_ids:
                data_object = {KEY_ENVIRONMENT: EnvironmentBuilder(id=environment_id).get_data(),
                               KEY_FUNCTION_ROLE_PERMISSION: self.parse_function_role_permission_array(environment_id)}
                data_array.append(data_object)
            return data_array
        except Exception as e:
            error_log(e)
            traceback.format_exc()

    def parse_function_role_permission_array(self, environment_id):
        array = []
        function_ids = Function.objects.all().values_list("id", flat=True)
        for function_id in function_ids:
            function_role_permission_object = {KEY_FUNCTION: FunctionBuilder(id=function_id).get_data(),
                                               KEY_ROLE_PERMISSION: self.parse_role_permission_array(environment_id,
                                                                                                     function_id)}
            array.append(function_role_permission_object)
        return array

    def parse_role_permission_array(self, environment_id, function_id):
        array = []
        role_type_ids = RoleType.objects.all().values_list("id", flat=True)
        for role_type_id in role_type_ids:
            role_type = RoleType.objects.get(id=role_type_id)
            role_permission_object = {KEY_ROLE_TYPE: RoleTypeBuilder(role_type).get_data()}
            try:
                role_permission_id = RolePermission.objects.filter_by_environment_role_type(environment_id,
                                                                                            role_type_id).first()
                role_function_permission = RoleFunctionPermission.objects.get(function_id=function_id,
                                                                              role_permission_id=role_permission_id)
                role_permission_object[KEY_VISIBLE] = role_function_permission.visible
                role_permission_object[KEY_EDITABLE] = role_function_permission.editable
            except RolePermission.DoesNotExist:
                role_permission_object[KEY_VISIBLE] = self.DISABLE
                role_permission_object[KEY_EDITABLE] = self.DISABLE
            except RoleFunctionPermission.DoesNotExist:
                role_permission_object[KEY_VISIBLE] = self.DISABLE
                role_permission_object[KEY_EDITABLE] = self.DISABLE

            array.append(role_permission_object)
        return array
