from django.contrib.auth.models import User
from permission.data_object.json_builder.base import SettingBaseBuilder
from permission.models import RolePermission, Environment, RoleType
from common.data_object.json_builder.user import UserBuilder


class UserRoleListBuilder(SettingBaseBuilder):

    def __init__(self, user):
        try:
            self.environment_ids = Environment.objects.all().values_list("id",flat=True)
            SettingBaseBuilder.__init__(self, user)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict["data"] = self.parse_user_role_objects()

    def parse_user_role_objects(self):
        array = []
        for user in User.objects.all():
            data = {
                "user": UserBuilder(user).get_data(),
                "environment_role": self.parse_environment_role(user)
            }
            array.append(data)
        return array

    def parse_environment_role(self, user):
        array = []
        role_permissions = RolePermission.objects.filter(environment_id__in=self.environment_ids,
                                                         user_role_permission_role_permission__user_id=user.id).values(
            "environment_id", "role_type").distinct()
        for role_permission in role_permissions:
            environment_role = {}
            environment = Environment.objects.get(id=role_permission.get("environment_id"))
            role_type = RoleType.objects.get(id=role_permission.get("role_type"))
            environment_role["environment"] = environment.name
            environment_role["country"] = "All"
            environment_role["role_type"] = role_type.display_name
            array.append(environment_role)
        return array
