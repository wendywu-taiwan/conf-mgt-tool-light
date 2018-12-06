import traceback
from RulesetComparer.utils import fileManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *
from RulesetComparer.models import Country, Environment, Function, Module, UserRole


def init_data():
    try:
        logging.info("init ruleset data")
        preload_data_path = settings.BASE_DIR + config.get_file_path("preload_data")
        preload_data = fileManager.load_json_file(preload_data_path)
        ruleset_data = preload_data["ruleset_data"]
        init_country_data(ruleset_data["country"])
        init_environment_data(ruleset_data["environment"])
        init_function_data(ruleset_data["function"])
        init_module_data(ruleset_data["module"])
        init_user_role_data(ruleset_data['user_role'])
    except Exception:
        Country.objects.all().delete()
        traceback.print_exc()
        logging.error(traceback.format_exc())

def init_country_data(country_list):
    db_countries = Country.objects.all()
    if len(db_countries) == 0:
        try:
            for country_obj in country_list:
                name = country_obj["name"]
                full_name = country_obj["full_name"]
                icon_file_name = country_obj["icon_file_name"]
                Country.objects.create_country(name, full_name, icon_file_name)
            logging.info("init country data success")
        except Exception as err:
            Country.objects.all().delete()
            logging.error(traceback.format_exc())
            print("init preload country data to DB fail , error:", err)


def init_environment_data(environment_data):
    db_environments = Environment.objects.all()
    if len(db_environments) == 0:
        try:
            for environment_obj in environment_data:
                name = environment_obj["name"]
                full_name = environment_obj["full_name"]
                client = environment_obj['b2b_rule_set_client']
                account = environment_obj['account']
                password = environment_obj['password']
                Environment.objects.create_environment(name, full_name, client, account, password)
            logging.info("init environment data success")
        except Exception as err:
            Environment.objects.all().delete()
            logging.error(traceback.format_exc())
            print("init preload country data to DB fail , error:", err)


def init_function_data(function_data):
    db_functions = Function.objects.all()
    if len(db_functions) == 0:
        try:
            for function_obj in function_data:
                name = function_obj["name"]
                icon_file_name = function_obj["icon_file_name"]
                Function.objects.create(name=name, icon_file_name=icon_file_name)
            logging.info("init function data success")
        except Exception as err:
            Function.objects.all().delete()
            logging.error(traceback.format_exc())
            print("init preload function data to DB fail , error:", err)


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
            logging.info("init module data success")
        except Exception as err:
            Module.objects.all().delete()
            logging.error(traceback.format_exc())
            print("init preload module data to DB fail , error:", err)


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
            logging.info("init user role data success")
        except Exception as err:
            UserRole.objects.all().delete()
            logging.error(traceback.format_exc())
            print("init preload user role data to DB fail , error:", err)
