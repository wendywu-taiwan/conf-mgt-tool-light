from permission.data_object.json_builder.role_permission_list import RolePermissionBuilder


def get_role_permission_list(user):
    data = RolePermissionBuilder(user).get_data()
    return data


def get_role_permission_edit():
    pass


def edit_role_permission():
    pass
