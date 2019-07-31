from permission.models import RolePermission, RoleFunctionPermission, UserRolePermission
from django.contrib.auth.models import User

VISIBLE = "visible"
EDITABLE = "editable"
LOG_CLASS = "permission_manager"


def enable_environments(user_id):
    user = User.objects.get(id=user_id)
    role_permission_list = UserRolePermission.objects.filter(user=user).values_list("role_permission_id", flat=True)
    enable_environments_ids = RolePermission.objects.filter(id__in=role_permission_list).values_list("environment_id", flat=True).distinct()
    return enable_environments_ids


def enable_countries(user_id, environment_id):
    user = User.objects.get(id=user_id)
    role_permission_list = UserRolePermission.objects.filter(user=user).values_list("role_permission_id", flat=True)
    country_list = RolePermission.objects.filter(id__in=role_permission_list,
                                                 environment_id=environment_id).values_list("country_id",
                                                                                            flat=True).distinct()
    return list(country_list)


def enable_environments_countries(user_id, environment_ids):
    user = User.objects.get(id=user_id)
    role_permission_list = UserRolePermission.objects.filter(user=user).values_list("role_permission_id", flat=True)
    country_list = RolePermission.objects.filter(id__in=role_permission_list,
                                                 environment_id__in=environment_ids).values_list("country_id",
                                                                                                 flat=True).distinct()
    return list(country_list)


def enable_functions(user_id):
    pass


def check_function_enable(user_id, function_id):
    user = User.objects.get(id=user_id)
    role_permission_list = UserRolePermission.objects.filter(user=user).values_list("role_permission_id", flat=True)
    count = RoleFunctionPermission.objects.filter(role_permission_id__in=role_permission_list,
                                                  function_id=function_id, visible=1).count()
    if count == 0:
        return False
    else:
        return True


def is_visible(user_id, environment_id, country_id, function_id):
    return is_enable(user_id, environment_id, country_id, function_id, VISIBLE)


def is_editable(user_id, environment_id, country_id, function_id):
    return is_enable(user_id, environment_id, country_id, function_id, EDITABLE)


def is_enable(user_id, environment_id, country_id, function_id, key):
    function_permission = get_permission(user_id, environment_id, country_id, function_id)
    if function_permission is None or function_permission.get(key) == 0:
        return False
    else:
        return True


def get_permission(user_id, environment_id, country_id, function_id):
    role_permission_id = RolePermission.objects.get_role_permission_by_user_env_country_id(user_id, environment_id,
                                                                                           country_id)
    role_function_permission = RoleFunctionPermission.objects.get_role_function_permission(role_permission_id,
                                                                                           function_id)
    return role_function_permission
