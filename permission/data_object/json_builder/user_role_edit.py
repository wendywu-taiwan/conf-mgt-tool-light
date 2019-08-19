from django.contrib.auth.models import User

from permission.data_object.json_builder.base import SettingBaseBuilder
from permission.models import Environment, RoleType, UserRolePermission
from permission.data_object.json_builder.role_type import RoleTypeBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.user import UserBuilder
from RulesetComparer.properties.key import *


class UserRoleEditBuilder(SettingBaseBuilder):

    def __init__(self, login_user, edit_user_id):
        try:
            self.edit_user = User.objects.get(id=edit_user_id)
            SettingBaseBuilder.__init__(self, login_user)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict["data"] = self.parser_data()

    def parser_data(self):
        data_array = []
        environments = Environment.objects.all()
        for environment in environments:
            data_object = {KEY_ENVIRONMENT: EnvironmentBuilder(environment=environment).get_data(),
                           KEY_ROLE_TYPE: self.parse_role_type_array(environment.id)}

            data_array.append(data_object)
        data = {
            KEY_USER_DATA: UserBuilder(self.edit_user).get_data(),
            KEY_ENVIRONMENT_ROLE: data_array
        }
        return data

    def parse_role_type_array(self, environment_id):
        array = []
        for role_type in RoleType.objects.all():
            role_type_data = RoleTypeBuilder(role_type).get_data()
            user_role_count = UserRolePermission.objects.filter(user_id=self.edit_user.id,
                                                                role_permission__environment__id=environment_id,
                                                                role_permission__role_type__id=role_type.id).count()
            if user_role_count == 0:
                role_type_data[KEY_CHECKED] = False
            else:
                role_type_data[KEY_CHECKED] = True

            array.append(role_type_data)
        return array
