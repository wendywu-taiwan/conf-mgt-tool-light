from permission.models import RoleFunctionPermission, RolePermission


class EditRolePermissionParser:
    def __init__(self, json_data):
        self.environment_id = json_data.get("environment_id")
        self.function_permissions = json_data.get("function_permissions")

    def parse_data(self):
        for function_permission in self.function_permissions:
            function_id = function_permission.get("function_id")
            permissions = function_permission.get("permissions")
            for permission in permissions:
                role_type_id = permission.get("role_type_id")
                visible = permission.get("visible")
                editable = permission.get("editable")
                RoleFunctionPermission.objects.filter(function_id=function_id,
                                                      role_permission__environment__id=self.environment_id,
                                                      role_permission__role_type__id=role_type_id).update(visible=visible, editable=editable)
