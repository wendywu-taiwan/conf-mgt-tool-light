import traceback
from RulesetComparer.utils import fileManager, modelManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from RulesetComparer.models import Country, Environment, Function, Module, UserRole
from RulesetComparer.services.services import restart_all_scheduler

LOG_CLASS = "initDataService"


def init_data(apps, schema_editor):
    try:
        debug_log(LOG_CLASS, "init ruleset data")
        preload_data_path = settings.BASE_DIR + config.get_file_path("preload_data")
        preload_data = fileManager.load_json_file(preload_data_path)
        ruleset_data = preload_data["ruleset_data"]
        has_country = init_country_data(ruleset_data["country"])
        has_environment = init_environment_data(ruleset_data["environment"])
        has_function = init_function_data(ruleset_data["function"])
        has_module = init_module_data(ruleset_data["module"])
        has_user_role = init_user_role_data(ruleset_data['user_role'])
        restart_all_scheduler()

    except Exception as e:
        Country.objects.all().delete()
        traceback.print_exc()
        error_log(traceback.format_exc())
        raise e


def init_country_data(country_list):
    db_countries = Country.objects.all()
    if len(db_countries) == 0:
        try:
            for country_obj in country_list:
                name = country_obj["name"]
                full_name = country_obj["full_name"]
                icon_file_name = country_obj["icon_file_name"]
                Country.objects.create_country(name, full_name, icon_file_name)
            debug_log(LOG_CLASS, "init country data success")
            return True
        except Exception as err:
            Country.objects.all().delete()
            error_log(traceback.format_exc())
            return False


def init_environment_data(environment_data):
    db_environments = Environment.objects.all()
    if len(db_environments) == 0:
        try:
            for environment_obj in environment_data:
                name = environment_obj["name"]
                full_name = environment_obj["full_name"]
                client = environment_obj['b2b_rule_set_client']
                Environment.objects.create_environment(name, full_name, client)
            debug_log(LOG_CLASS, "init environment data success")
            return True
        except Exception as err:
            Environment.objects.all().delete()
            error_log(traceback.format_exc())
            print("init preload country data to DB fail , error:", err)
            return False


def init_function_data(function_data):
    db_functions = Function.objects.all()
    if len(db_functions) == 0:
        try:
            for function_obj in function_data:
                name = function_obj["name"]
                icon_file_name = function_obj["icon_file_name"]
                Function.objects.create(name=name, icon_file_name=icon_file_name)
            debug_log(LOG_CLASS, "init function data success")
            return True
        except Exception:
            Function.objects.all().delete()
            error_log(traceback.format_exc())
            return False


def init_module_data(module_data):
    db_modules = Module.objects.all()
    if len(db_modules) == 0:
        try:
            for module_obj in module_data:
                name = module_obj['name']
                module = Module.objects.create(name=name)
                function_list = module_obj['functions']
                for function_name in function_list:
                    db_function = Function.objects.get(name=function_name)
                    if db_function is None:
                        continue
                    module.functions.add(db_function)
            debug_log(LOG_CLASS, "init module data success")
            return True
        except Exception as err:
            Module.objects.all().delete()
            error_log(traceback.format_exc())
            print("init preload module data to DB fail , error:", err)
            return False


def init_user_role_data(user_role_data):
    db_user_roles = UserRole.objects.all()
    if len(db_user_roles) == 0:
        try:
            for user_role_obj in user_role_data:
                name = user_role_obj['name']
                user_role = UserRole.objects.create(name=name)
                module_list = user_role_obj['modules']
                for module_name in module_list:
                    db_module = Module.objects.get(name=module_name)
                    if db_module is None:
                        continue
                    user_role.modules.add(db_module)
            debug_log(LOG_CLASS, "init user role data success")
            return True
        except Exception as err:
            UserRole.objects.all().delete()
            error_log(traceback.format_exc())
            print("init preload user role data to DB fail , error:", err)
            return False
