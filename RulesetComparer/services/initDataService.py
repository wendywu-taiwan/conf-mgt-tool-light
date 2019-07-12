import traceback
from RulesetComparer.utils import fileManager, modelManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from RulesetComparer.models import Country, Environment, Function, Module, UserRole, DataCenter, B2BService, B2BClient, \
    B2BServer, DataUpdateTime, MailContentType, RulesetAction
from django.contrib.auth.models import User

LOG_CLASS = "initDataService"

KEY_AUTH_USER = "auth_user"
KEY_MAIL_CONTENT_TYPE = "mail_content_type"
KEY_COUNTRY = "country"
KEY_ENVIRONMENT = "environment"
KEY_FUNCTION = "function"
KEY_MODULE = "module"
KEY_USER_ROLE = "user_role"
KEY_DATA_CENTER = "data_center"
KEY_B2B_SERVICE = "b2b_service"
KEY_B2B_CLIENT = "b2b_client"
KEY_B2B_SERVER = "b2b_server"
KEY_RULESET_ACTION = "ruleset_action"


def init_data():
    try:
        info_log(LOG_CLASS, "init ruleset data")
        preload_data_path = settings.BASE_DIR + config.get_file_path("preload_data")
        preload_data = fileManager.load_json_file(preload_data_path)
        ruleset_data = preload_data["ruleset_data"]
        update_time_data = ruleset_data["update_time"]

        if has_update(update_time_data, KEY_AUTH_USER):
            info_log(LOG_CLASS, "auth_user has update")
            update_auth_user = init_auth_user_data(ruleset_data[KEY_AUTH_USER])
            if update_auth_user:
                update_local_time(update_time_data, KEY_AUTH_USER)

        if has_update(update_time_data, KEY_MAIL_CONTENT_TYPE):
            update_mail_content = init_mail_content_type_data(ruleset_data[KEY_MAIL_CONTENT_TYPE])
            if update_mail_content:
                update_local_time(update_time_data, KEY_MAIL_CONTENT_TYPE)

        if has_update(update_time_data, KEY_COUNTRY):
            update_country = init_country_data(ruleset_data[KEY_COUNTRY])
            if update_country:
                update_local_time(update_time_data, KEY_COUNTRY)

        if has_update(update_time_data, KEY_ENVIRONMENT):
            info_log(LOG_CLASS, "environment has update")
            update_environment = init_environment_data(ruleset_data[KEY_ENVIRONMENT])
            if update_environment:
                update_local_time(update_time_data, KEY_ENVIRONMENT)

        if has_update(update_time_data, KEY_FUNCTION):
            update_function = init_function_data(ruleset_data[KEY_FUNCTION])
            if update_function:
                update_local_time(update_time_data, KEY_FUNCTION)

        if has_update(update_time_data, KEY_MODULE):
            update_module = init_module_data(ruleset_data[KEY_MODULE])
            if update_module:
                update_local_time(update_time_data, KEY_MODULE)

        if has_update(update_time_data, KEY_USER_ROLE):
            update_user_role = init_user_role_data(ruleset_data[KEY_USER_ROLE])
            if update_user_role:
                update_local_time(update_time_data, KEY_USER_ROLE)

        if has_update(update_time_data, KEY_DATA_CENTER):
            update_data_center = init_data_center(ruleset_data[KEY_DATA_CENTER])
            if update_data_center:
                update_local_time(update_time_data, KEY_DATA_CENTER)

        if has_update(update_time_data, KEY_B2B_SERVICE):
            update_b2b_service = init_b2b_service(ruleset_data[KEY_B2B_SERVICE])
            if update_b2b_service:
                update_local_time(update_time_data, KEY_B2B_SERVICE)

        if has_update(update_time_data, KEY_B2B_CLIENT):
            update_b2b_client = init_b2b_client(ruleset_data[KEY_B2B_CLIENT])
            if update_b2b_client:
                update_local_time(update_time_data, KEY_B2B_CLIENT)

        if has_update(update_time_data, KEY_B2B_SERVER):
            update_b2b_server = init_b2b_server(ruleset_data[KEY_B2B_SERVER])
            if update_b2b_server:
                update_local_time(update_time_data, KEY_B2B_SERVER)

        if has_update(update_time_data, KEY_RULESET_ACTION):
            info_log(LOG_CLASS, "rulesetaction has update")
            update_ruleset_action = init_ruleset_action(ruleset_data[KEY_RULESET_ACTION])
            if update_ruleset_action:
                update_local_time(update_time_data, KEY_RULESET_ACTION)
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def init_auth_user_data(auth_user_data):
    try:

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
    except Exception as e:
        raise e


def init_mail_content_type_data(mail_content_types):
    try:
        for mail_content_type in mail_content_types:
            name = mail_content_type["name"]
            title = mail_content_type["title"]

            if MailContentType.objects.filter(name=name).exists():
                MailContentType.objects.filter(name=name).update(title=title)
            else:
                MailContentType.objects.create(name=name, title=title)

        info_log(LOG_CLASS, "init mail content data success")
        return True
    except Exception as e:
        raise e


def init_country_data(country_list):
    try:
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
    except Exception as e:
        raise e


def init_environment_data(environment_data):
    try:
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
    except Exception as e:
        raise e


def init_function_data(function_data):
    try:
        for function_obj in function_data:
            name = function_obj["name"]
            icon_file_name = function_obj["icon_file_name"]

            if Function.objects.filter(name=name).exists():
                Function.objects.filter(name=name).update(icon_file_name=icon_file_name)
            else:
                Function.objects.create(name=name, icon_file_name=icon_file_name)
        info_log(LOG_CLASS, "init function data success")
        return True
    except Exception as e:
        raise e


def init_module_data(module_data):
    try:
        for module_obj in module_data:
            name = module_obj['name']

            if Module.objects.filter(name=name).exists():
                module = Module.objects.get(name=name)
            else:
                module = Module.objects.create(name=name)

            function_list = module_obj['functions']
            for function_name in function_list:
                db_function = Function.objects.get(name=function_name)
                if db_function is None:
                    continue
                module.functions.add(db_function)

        info_log(LOG_CLASS, "init module data success")
        return True
    except Exception as e:
        raise e


def init_user_role_data(user_role_data):
    try:
        for user_role_obj in user_role_data:
            name = user_role_obj['name']

            if UserRole.objects.filter(name=name).exists():
                user_role = UserRole.objects.get(name=name)
            else:
                user_role = UserRole.objects.create(name=name)

            module_list = user_role_obj['modules']
            for module_name in module_list:
                db_module = Module.objects.get(name=module_name)
                if db_module is None:
                    continue
                user_role.modules.add(db_module)
        info_log(LOG_CLASS, "init user role data success")
        return True
    except Exception as e:
        raise e


def init_data_center(data_center_data):
    try:
        for data_center_obj in data_center_data:
            name = data_center_obj['name']

            if DataCenter.objects.filter(name=name).exists():
                pass
            else:
                DataCenter.objects.create(name=name)
        info_log(LOG_CLASS, "init data center data success")
        return True
    except Exception as e:
        raise e


def init_b2b_service(b2b_service_data):
    try:
        for b2b_service_obj in b2b_service_data:
            name = b2b_service_obj['name']
            url = b2b_service_obj['url']

            if B2BService.objects.filter(url=url).exists():
                pass
            else:
                B2BService.objects.create(name=name, url=url)

        info_log(LOG_CLASS, "init b2b service data success")
        return True
    except Exception as e:
        raise e


def init_b2b_client(b2b_client_data):
    try:
        for b2b_client_obj in b2b_client_data:
            data_center = DataCenter.objects.get(name=b2b_client_obj["data_center"])
            url = b2b_client_obj["url"]

            if B2BClient.objects.filter(url=url).exists():
                pass
            else:
                B2BClient.objects.create(data_center=data_center, url=url)

        info_log(LOG_CLASS, "init b2b client data success")
        return True
    except Exception as e:
        raise e


def init_b2b_server(b2b_server_data):
    try:
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
    except Exception as e:
        raise e


def init_ruleset_action(ruleset_action_data):
    try:
        for ruleset_action in ruleset_action_data:
            name = ruleset_action["name"]
            capital_name = ruleset_action["capital_name"]

            if RulesetAction.objects.filter(name=name).exists():
                RulesetAction.objects.filter(name=name).update(capital_name=capital_name)
            else:
                RulesetAction.objects.create(name=name, capital_name=capital_name)
        info_log(LOG_CLASS, "init ruleset action data success")
        return True
    except Exception as e:
        raise e


def get_date_time(time):
    time_format = config.TIME_FORMAT.get('db_time_format')
    date_time = timeUtil.time_to_date_time(time, time_format)
    return date_time


def get_db_date_time(time):
    time_format = config.TIME_FORMAT.get('db_time_format')
    date_time = timeUtil.date_time_change_format(time, time_format)
    return date_time


def update_local_time(update_time_data, table_name):
    new_date_time = get_date_time(update_time_data[table_name]["update_time"])
    info_log(LOG_CLASS, "update " + table_name + " time:" + str(new_date_time))
    if DataUpdateTime.objects.filter(table=table_name).exists():
        DataUpdateTime.objects.filter(table=table_name).update(update_time=new_date_time)
    else:
        DataUpdateTime.objects.create(table=table_name, update_time=new_date_time)


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
