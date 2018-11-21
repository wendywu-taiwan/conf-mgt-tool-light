from RulesetComparer.models import Country, Environment
from RulesetComparer.utils import fileManager
from RulesetComparer.properties import config
from django.conf import settings


class InitDataService(object):
    def __init__(self):
        preload_data_path = settings.BASE_DIR + config.get_file_path("preload_data")
        preload_data = fileManager.load_json_file(preload_data_path)
        self.ruleset_data = preload_data["ruleset_data"]
        self.init_country_data()
        self.init_environment_data()

    def init_country_data(self):
        country_list = self.ruleset_data["country"]
        db_countries = Country.objects.all()
        if len(db_countries) == 0:
            try:
                for country_obj in country_list:
                    name = country_obj["name"]
                    full_name = country_obj["full_name"]
                    Country.objects.create_country(name, full_name)
            except Exception as err:
                Country.objects.all().delete()
                print("insert preload country data to DB fail , error:", err)

    def init_environment_data(self):
        environment_list = self.ruleset_data["environment"]
        db_environments = Environment.objects.all()
        if len(db_environments) == 0:
            try:
                for environment_obj in environment_list:
                    name = environment_obj["name"]
                    full_name = environment_obj["full_name"]
                    client = environment_obj['b2b_rule_set_client']
                    account = environment_obj['account']
                    password = environment_obj['password']
                    Environment.objects.create_environment(name, full_name, client, account, password)
            except Exception as err:
                Environment.objects.all().delete()
                print("insert preload country data to DB fail , error:", err)
