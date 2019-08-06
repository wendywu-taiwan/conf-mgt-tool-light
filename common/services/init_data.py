import traceback
from RulesetComparer.utils import fileManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from permission.models import Environment, Country, Module, Function, DataCenter, B2BServer, B2BService, B2BClient, \
    RoleType, RolePermission, RoleFunctionPermission, UserRolePermission
from common.models import DataUpdateTime
from RulesetComparer.models import MailContentType, RulesetAction
from django.contrib.auth.models import User

LOG_CLASS = "initDataService"

# permission module
KEY_AUTH_USER = "auth_user"
KEY_COUNTRY = "country"
KEY_ENVIRONMENT = "environment"
KEY_MODULE = "module"
KEY_FUNCTION = "function"
KEY_ROLE_TYPE = "role_type"
KEY_ROLE_PERMISSION = "role_permission"
KEY_USER_ROLE_PERMISSION = "user_role_permission"
KEY_ROLE_FUNCTION_PERMISSION = "role_function_permission"
KEY_DATA_CENTER = "data_center"
KEY_B2B_SERVICE = "b2b_service"
KEY_B2B_CLIENT = "b2b_client"
KEY_B2B_SERVER = "b2b_server"
# ruleset module
KEY_MAIL_CONTENT_TYPE = "mail_content_type"
KEY_RULESET_ACTION = "ruleset_action"


def init_auth_user_data(auth_user_data):
    for user in auth_user_data:
        username = user.get("username")
        password = user.get("password")
        email = user.get("email")
        is_superuser = user.get("is_superuser")
        is_staff = user.get("is_staff")
        is_active = user.get("is_active")

        if User.objects.filter(username=username).exists():
            user_obj = User.objects.get(username=username)
            user_obj.set_password(password)
            user_obj.email = email
            user_obj.save()
        else:
            user_obj = User.objects.create(username=username, email=email, is_superuser=is_superuser,
                                           is_staff=is_staff, is_active=is_active)
            user_obj.set_password(password)
            user_obj.save()
    info_log(LOG_CLASS, "init auth user data success")
    return True


def init_mail_content_type_data(mail_content_types):
    for mail_content_type in mail_content_types:
        name = mail_content_type["name"]
        title = mail_content_type["title"]

        if MailContentType.objects.filter(name=name).exists():
            MailContentType.objects.filter(name=name).update(title=title)
        else:
            MailContentType.objects.create(name=name, title=title)

    info_log(LOG_CLASS, "init mail content data success")
    return True


def init_country_data(country_list):
    for country_obj in country_list:
        name = country_obj["name"]
        full_name = country_obj["full_name"]
        icon_file_name = country_obj["icon_file_name"]

        if Country.objects.filter(name=name, full_name=full_name).exists():
            Country.objects.filter(name=name).update(full_name=full_name, icon_file_name=icon_file_name)
        else:
            Country.objects.create(name=name, full_name=full_name, icon_file_name=icon_file_name)

    info_log(LOG_CLASS, "init country data success")
    return True


def init_environment_data(environment_data):
    for environment_obj in environment_data:
        name = environment_obj.get("name")
        full_name = environment_obj.get("full_name")
        active = environment_obj.get("active")
        if Environment.objects.filter(name=name).exists():
            Environment.objects.filter(name=name).update(full_name=full_name, active=active)
        else:
            Environment.objects.create(name=name, full_name=full_name, active=active)
    info_log(LOG_CLASS, "init environment data success")
    return True


def init_module_data(data):
    for module_data in data:
        name = module_data.get("name")
        display_name = module_data.get("display_name")

        if Module.objects.filter(name=name).exists():
            Module.objects.filter(name=name).update(display_name=display_name)
        else:
            Module.objects.create(name=name, display_name=display_name)

    info_log(LOG_CLASS, "init module data success")
    return True


def init_function_data(data):
    for function_data in data:
        name = function_data.get("name")
        icon_file_name = function_data.get("icon_file_name")
        module_name = function_data.get("module_name")
        module = Module.objects.get(name=module_name)

        if Function.objects.filter(name=name, module=module).exists():
            Function.objects.filter(name=name).update(icon_file_name=icon_file_name)
        else:
            Function.objects.create(name=name, icon_file_name=icon_file_name, module=module)
    info_log(LOG_CLASS, "init function data success")
    return True


def init_role_type(data):
    for group_data in data:
        name = group_data.get("name")
        display_name = group_data.get("display_name")

        if RoleType.objects.filter(name=name).exists():
            RoleType.objects.filter(name=name).update(display_name=display_name)
        else:
            RoleType.objects.create(name=name, display_name=display_name)
    info_log(LOG_CLASS, "init permission role data success")
    return True


def init_role_permission(data):
    environments = Environment.objects.all()
    countries = Country.objects.all()
    role_types = RoleType.objects.all()
    for role_type in role_types:
        for environment in environments:
            for country in countries:
                if not RolePermission.objects.filter(role_type=role_type, environment=environment,
                                                     country=country).exists():
                    RolePermission.objects.create(role_type=role_type, environment=environment,
                                                  country=country)
    return True


def init_role_function_permission(data):
    for role_function_permission_obj in data:
        environment_name = role_function_permission_obj.get("environment_name")
        print("role_function_permission_obj, environment:" + environment_name)
        country_name = role_function_permission_obj.get("country_name")

        for rule_module_permission in role_function_permission_obj.get("role_module_permission"):
            module_name = rule_module_permission.get("module_name")
            permissions = rule_module_permission.get("permissions")
            for role_function_permission in permissions:
                role_type_name = role_function_permission.get("role_type")
                function_permission_array = role_function_permission.get("function_permission")

                if country_name == "all":
                    countries = Country.objects.all()
                    for country in countries:
                        role_permission = RolePermission.objects.get_role_permission(role_type_name, environment_name,
                                                                                     country.name)
                        create_or_update_role_permission(role_permission, function_permission_array, module_name)
                else:
                    role_permission = RolePermission.objects.get_role_permission(role_type_name, environment_name,
                                                                                 country_name)
                    create_or_update_role_permission(role_permission, function_permission_array, module_name)
    return True


def create_or_update_role_permission(role_permission, function_array, module_name):
    for function_option in function_array:
        function_name = function_option.get("function_name")
        visible = function_option.get("visible")
        editable = function_option.get("editable")
        function = Function.objects.get_function(module_name, function_name)

        if visible == "true":
            visible = 1
        else:
            visible = 0

        if editable == "true":
            editable = 1
        else:
            editable = 0

        if RoleFunctionPermission.objects.filter(role_permission=role_permission,
                                                 function=function).exists():
            RoleFunctionPermission.objects.filter(role_permission=role_permission,
                                                  function=function).update(visible=visible,
                                                                            editable=editable)
        else:
            RoleFunctionPermission.objects.create(role_permission=role_permission,
                                                  function=function, visible=visible, editable=editable)


def init_user_role_permission(data):
    for user_role_permission in data:
        user_name = user_role_permission.get("user_name")
        user = User.objects.get(username=user_name)
        permissions = user_role_permission.get("permission")
        for permission in permissions:
            environment_name = permission.get("environment")
            country_name = permission.get("country")
            role_type = permission.get("role_type")

            if country_name == "all":
                countries = Country.objects.all()
                for country in countries:
                    role_permission = RolePermission.objects.get_role_permission(role_type, environment_name,
                                                                                 country.name)
                    create_user_role_permission(user, role_permission)
            else:
                role_permission = RolePermission.objects.get_role_permission(role_type, environment_name, country_name)
                create_user_role_permission(user, role_permission)
    return True


def create_user_role_permission(user, role_permission):
    if not UserRolePermission.objects.filter(user=user, role_permission=role_permission).exists():
        UserRolePermission.objects.create(user=user, role_permission=role_permission)


def init_data_center(data_center_data):
    for data_center_obj in data_center_data:
        name = data_center_obj['name']

        if DataCenter.objects.filter(name=name).exists():
            pass
        else:
            DataCenter.objects.create(name=name)
    info_log(LOG_CLASS, "init data center data success")
    return True


def init_b2b_service(b2b_service_data):
    for b2b_service_obj in b2b_service_data:
        name = b2b_service_obj['name']
        url = b2b_service_obj['url']

        if B2BService.objects.filter(url=url).exists():
            pass
        else:
            B2BService.objects.create(name=name, url=url)

    info_log(LOG_CLASS, "init b2b service data success")
    return True


def init_b2b_client(b2b_client_data):
    for b2b_client_obj in b2b_client_data:
        data_center = DataCenter.objects.get(name=b2b_client_obj["data_center"])
        url = b2b_client_obj["url"]

        if B2BClient.objects.filter(url=url).exists():
            pass
        else:
            B2BClient.objects.create(data_center=data_center, url=url)

    info_log(LOG_CLASS, "init b2b client data success")
    return True


def init_b2b_server(b2b_server_data):
    for b2b_server_obj in b2b_server_data:
        country_name_list = b2b_server_obj["country_name"]
        environment = Environment.objects.get(name=b2b_server_obj["environment_name"])
        b2b_client = B2BClient.objects.get(url=b2b_server_obj["b2b_client_url"])
        for country_name in country_name_list:
            country = Country.objects.get(name=country_name)

            if B2BServer.objects.filter(country=country, environment=environment).exists():
                B2BServer.objects.filter(country=country, environment=environment).update(client=b2b_client)
            else:
                B2BServer.objects.create(country=country, environment=environment, client=b2b_client)

    info_log(LOG_CLASS, "init b2b server data success")
    return True


def init_ruleset_action(ruleset_action_data):
    for ruleset_action in ruleset_action_data:
        name = ruleset_action["name"]
        capital_name = ruleset_action["capital_name"]

        if RulesetAction.objects.filter(name=name).exists():
            RulesetAction.objects.filter(name=name).update(capital_name=capital_name)
        else:
            RulesetAction.objects.create(name=name, capital_name=capital_name)
    info_log(LOG_CLASS, "init ruleset action data success")
    return True


operator = {
    KEY_AUTH_USER: init_auth_user_data,
    KEY_ENVIRONMENT: init_environment_data,
    KEY_COUNTRY: init_country_data,
    KEY_MODULE: init_module_data,
    KEY_FUNCTION: init_function_data,
    KEY_ROLE_TYPE: init_role_type,
    KEY_ROLE_PERMISSION: init_role_permission,
    KEY_ROLE_FUNCTION_PERMISSION: init_role_function_permission,
    KEY_USER_ROLE_PERMISSION: init_user_role_permission,
    KEY_DATA_CENTER: init_data_center,
    KEY_B2B_SERVICE: init_b2b_service,
    KEY_B2B_CLIENT: init_b2b_client,
    KEY_B2B_SERVER: init_b2b_server,
    KEY_MAIL_CONTENT_TYPE: init_mail_content_type_data,
    KEY_RULESET_ACTION: init_ruleset_action
}

INIT_DATA_ARRAY = [KEY_AUTH_USER, KEY_ENVIRONMENT, KEY_COUNTRY,
                   KEY_MODULE, KEY_FUNCTION, KEY_ROLE_TYPE, KEY_ROLE_PERMISSION,
                   KEY_DATA_CENTER, KEY_B2B_SERVICE, KEY_B2B_CLIENT,
                   KEY_B2B_SERVER, KEY_MAIL_CONTENT_TYPE, KEY_RULESET_ACTION]


def init_data():
    try:
        info_log(LOG_CLASS, "init data")
        # load preload data
        preload_data_path = settings.BASE_DIR + config.get_file_path("preload_data")
        preload_data = fileManager.load_json_file(preload_data_path)
        data = preload_data["data"]

        # load role function permission data
        role_function_permission_data_path = settings.BASE_DIR + config.get_file_path("role_function_permission_data")
        role_function_permission_data = fileManager.load_json_file(role_function_permission_data_path)

        # load user role permission data
        user_role_permission_data_path = settings.BASE_DIR + config.get_file_path("user_role_permission_data")
        user_role_permission_data = fileManager.load_json_file(user_role_permission_data_path)

        for key in INIT_DATA_ARRAY:
            update_data(data, key)

        update_data(role_function_permission_data, KEY_ROLE_FUNCTION_PERMISSION)
        update_data(user_role_permission_data, KEY_USER_ROLE_PERMISSION)
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def update_data(data, key):
    update_time_data = data["update_time"]
    if has_update(update_time_data, key):
        info_log(LOG_CLASS, key + " has update")
        update_success = operator.get(key)(data.get(key))
        if update_success:
            update_local_time(update_time_data, key)


def has_update(update_time_data, table_name):
    local_update_time_obj = DataUpdateTime.objects.get_data_update_time(table_name)
    info_log(LOG_CLASS, "has_update , table_name:" + table_name)
    if local_update_time_obj is None:
        return True

    local_update_time = get_db_date_time(local_update_time_obj.update_time)
    new_update_time = get_date_time(update_time_data[table_name]["update_time"])

    if new_update_time > local_update_time:
        info_log(LOG_CLASS, table_name + " need update")
        return True
    else:
        info_log(LOG_CLASS, table_name + " no need update")
        return False


def update_local_time(update_time_data, table_name):
    new_date_time = get_date_time(update_time_data[table_name]["update_time"])
    info_log(LOG_CLASS, "update " + table_name + " time:" + str(new_date_time))
    if DataUpdateTime.objects.filter(table=table_name).exists():
        DataUpdateTime.objects.filter(table=table_name).update(update_time=new_date_time)
    else:
        DataUpdateTime.objects.create(table=table_name, update_time=new_date_time)


def get_date_time(time):
    time_format = config.TIME_FORMAT.get('db_time_format')
    date_time = timeUtil.time_to_date_time(time, time_format)
    return date_time


def get_db_date_time(time):
    time_format = config.TIME_FORMAT.get('db_time_format')
    date_time = timeUtil.date_time_change_format(time, time_format)
    return date_time
