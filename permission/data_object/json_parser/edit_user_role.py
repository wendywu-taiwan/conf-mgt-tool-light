from permission.models import UserRolePermission, RolePermission


class EditUserRoleParser:
    def __init__(self, json_data):
        self.user_id = json_data.get("user_id")
        self.checked_list = json_data.get("checked_list")

    def parse_data(self):
        # remove exist user role permission
        UserRolePermission.objects.filter(user_id=self.user_id).delete()
        for checked_data in self.checked_list:
            environment_id = checked_data.get("environment_id")
            role_type_id = checked_data.get("role_type_id")
            role_permission_ids = RolePermission.objects.filter(environment_id=environment_id,
                                                                role_type_id=role_type_id).values_list("id", flat=True)
            # add new user role permission
            for role_permission_id in role_permission_ids:
                UserRolePermission.objects.create(user_id=self.user_id, role_permission_id=role_permission_id)
