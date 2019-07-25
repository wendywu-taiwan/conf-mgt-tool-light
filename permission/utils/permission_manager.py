from permission.models import RolePermission, RoleFunctionPermission

VISIBLE = "visible"
EDITABLE = "editable"
LOG_CLASS = "permission_manager"


def enable_environments(user_id):
    pass


def enable_countries(user_id, environment_id):
    pass


def enable_functions(user_id):
    pass


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
