from permission.data_object.json_builder.base import SettingBaseBuilder
from permission.models import RolePermission, Environment, RoleType, UserRolePermission
from permission.data_object.json_builder.role_type import RoleTypeBuilder
from RulesetComparer.properties.key import *
from RulesetComparer.date_model.json_builder.environment import EnvironmentBuilder


class UserRoleEditBuilder(SettingBaseBuilder):

    def __init__(self, user):
        try:
            self.user = user
            SettingBaseBuilder.__init__(self, user)
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
        return data_array

    def parse_role_type_array(self, environment_id):
        array = []
        for role_type in RoleType.objects.all():
            role_type_data = RoleTypeBuilder(role_type).get_data()
            user_role_count = UserRolePermission.objects.filter(user_id=self.user.id,
                                                                role_permission__environment__id=environment_id,
                                                                role_permission__role_type__id=role_type.id).count()
            if user_role_count == 0:
                role_type_data[KEY_CHECKED] = False
            else:
                role_type_data[KEY_CHECKED] = True

            array.append(role_type_data)
        return array
