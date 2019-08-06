from permission.models import RolePermission, Function
from RulesetComparer.properties.key import *
from permission.data_object.json_builder.user_role_list import UserRoleListBuilder


def get_user_role_list(user):
    function_id = Function.objects.get(name=KEY_F_USER_ROLE).id
    environment_ids = RolePermission.objects.filter(role_function_role_permission__function__id=function_id,
                                                    role_function_role_permission__visible=1,
                                                    role_function_role_permission__editable=1,
                                                    user_role_permission_role_permission__user_id=user.id).values_list("environment_id", flat=True).distinct()

    data = UserRoleListBuilder(user, environment_ids).get_data()
    return data
