from permission.data_object.json_builder.role_permission_list import RolePermissionBuilder
from permission.data_object.json_builder.role_permission_edit import RolePermissionEditBuilder
from permission.data_object.json_parser.edit_role_permission import EditRolePermissionParser


def get_role_permission_list(user):
    data = RolePermissionBuilder(user).get_data()
    return data


def get_role_permission_edit(user, environment_id):
    data = RolePermissionEditBuilder(user, environment_id).get_data()
    return data


def edit_role_permission_data(json_data):
    parser = EditRolePermissionParser(json_data)
    parser.parse_data()
