from permission.data_object.json_builder.user_role_list import UserRoleListBuilder
from permission.data_object.json_builder.user_role_edit import UserRoleEditBuilder
from permission.data_object.json_parser.edit_user_role import EditUserRoleParser


def get_user_role_list(user):
    data = UserRoleListBuilder(user).get_data()
    return data


def get_user_role_edit(login_user, edit_user_id):
    data = UserRoleEditBuilder(login_user, edit_user_id).get_data()
    return data


def edit_user_role_data(json_data):
    parser = EditUserRoleParser(json_data)
    parser.parse_data()
