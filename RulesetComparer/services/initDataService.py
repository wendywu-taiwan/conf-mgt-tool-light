import traceback
from RulesetComparer.utils import fileManager, modelManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from RulesetComparer.models import Country, Environment, Function, Module, UserRole, DataCenter, B2BService, B2BClient, \
    B2BServer, DataUpdateTime, MailContentType

LOG_CLASS = "initDataService"

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


def init_data():
    try:
        info_log(LOG_CLASS, "init ruleset data")
        preload_data_path = settings.BASE_DIR + config.get_file_path("preload_data")
        preload_data = fileManager.load_json_file(preload_data_path)
        ruleset_data = preload_data["ruleset_data"]
        update_time_data = ruleset_data["update_time"]

        if has_update(update_time_data, KEY_MAIL_CONTENT_TYPE):
            update_mail_content = init_mail_content_type_data(ruleset_data[KEY_MAIL_CONTENT_TYPE])
            if update_mail_content:
                update_local_time(update_time_data, KEY_MAIL_CONTENT_TYPE)

        if has_update(update_time_data, KEY_COUNTRY):
            update_country = init_country_data(ruleset_data[KEY_COUNTRY])
            if update_country:
                update_local_time(update_time_data, KEY_COUNTRY)

        if has_update(update_time_data, KEY_ENVIRONMENT):
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
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def init_mail_content_type_data(mail_content_types):
    try:
        MailContentType.objects.all().delete()
        for mail_content_type in mail_content_types:
            name = mail_content_type["name"]
            title = mail_content_type["title"]
            MailContentType.objects.create(name=name, title=title)
        info_log(LOG_CLASS, "init mail content data success")
        return True
    except Exception as e:
        MailContentType.objects.all().delete()
        raise e


def init_country_data(country_list):
    try:
        Country.objects.all().delete()
        for country_obj in country_list:
            name = country_obj["name"]
            full_name = country_obj["full_name"]
            icon_file_name = country_obj["icon_file_name"]
            Country.objects.create_country(name, full_name, icon_file_name)
        info_log(LOG_CLASS, "init country data success")
        return True
    except Exception as e:
        Country.objects.all().delete()
        raise e


def init_environment_data(environment_data):
    try:
        Environment.objects.all().delete()
        for environment_obj in environment_data:
            name = environment_obj["name"]
            full_name = environment_obj["full_name"]
            Environment.objects.create_environment(name, full_name)
        info_log(LOG_CLASS, "init environment data success")
        return True
    except Exception as e:
        Environment.objects.all().delete()
        raise e


def init_function_data(function_data):
    try:
        Function.objects.all().delete()
        for function_obj in function_data:
            name = function_obj["name"]
            icon_file_name = function_obj["icon_file_name"]
            Function.objects.create(name=name, icon_file_name=icon_file_name)
        info_log(LOG_CLASS, "init function data success")
        return True
    except Exception as e:
        Function.objects.all().delete()
        raise e


def init_module_data(module_data):
    try:
        Module.objects.all().delete()
        for module_obj in module_data:
            name = module_obj['name']
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
        Module.objects.all().delete()
        raise e


def init_user_role_data(user_role_data):
    try:
        UserRole.objects.all().delete()
        for user_role_obj in user_role_data:
            name = user_role_obj['name']
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
        UserRole.objects.all().delete()
        raise e


def init_data_center(data_center_data):
    try:
        DataCenter.objects.all().delete()
        for data_center_obj in data_center_data:
            name = data_center_obj['name']
            DataCenter.objects.create(name=name)

        info_log(LOG_CLASS, "init data center data success")
        return True
    except Exception as e:
        DataCenter.objects.all().delete()
        raise e


def init_b2b_service(b2b_service_data):
    try:
        B2BService.objects.all().delete()
        for b2b_service_obj in b2b_service_data:
            name = b2b_service_obj['name']
            url = b2b_service_obj['url']
            B2BService.objects.create(name=name, url=url)

        info_log(LOG_CLASS, "init b2b service data success")
        return True
    except Exception as e:
        B2BService.objects.all().delete()
        raise e


def init_b2b_client(b2b_client_data):
    try:
        B2BClient.objects.all().delete()
        for b2b_client_obj in b2b_client_data:
            data_center = DataCenter.objects.get(name=b2b_client_obj["data_center"])
            url = b2b_client_obj["url"]
            B2BClient.objects.create(data_center=data_center, url=url)

        info_log(LOG_CLASS, "init b2b client data success")
        return True
    except Exception as e:
        B2BClient.objects.all().delete()
        raise e


def init_b2b_server(b2b_server_data):
    try:
        B2BServer.objects.all().delete()
        for b2b_server_obj in b2b_server_data:
            country_name_list = b2b_server_obj["country_name"]
            environment = Environment.objects.get(name=b2b_server_obj["environment_name"])
            b2b_client = B2BClient.objects.get(url=b2b_server_obj["b2b_client_url"])
            for country_name in country_name_list:
                country = Country.objects.get(name=country_name)
                B2BServer.objects.create(country=country, environment=environment, client=b2b_client)

        info_log(LOG_CLASS, "init b2b server data success")
        return True
    except Exception as e:
        B2BServer.objects.all().delete()
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
    local_update_time = DataUpdateTime.objects.get_data_update_time(table_name)

    new_date_time = get_date_time(update_time_data[table_name]["update_time"])
    info_log(LOG_CLASS, "update " + table_name + " time:" + str(new_date_time))
    if local_update_time is None:
        DataUpdateTime.objects.create(table=table_name, update_time=new_date_time)
    else:
        local_update_time.update_time = new_date_time
        local_update_time.save()


def has_update(update_time_data, table_name):
    local_update_time_obj = DataUpdateTime.objects.get_data_update_time(table_name)

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
