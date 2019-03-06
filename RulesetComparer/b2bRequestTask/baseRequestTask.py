import traceback
from zeep import Client
from abc import abstractmethod
from RulesetComparer.utils.logger import *
from RulesetComparer.models import Country, Environment
from RulesetComparer.dataModel.dataParser.authDataParser import AuthDataParser


class BaseRequestTask:

    def __init__(self):
        self.country = None
        self.environment = None
        self.auth_data = None
        self.client = None
        self.b2b_response_data = None

    def parse_data(self, environment_id, country_id):
        try:
            self.country = Country.objects.get(id=country_id)
            self.environment = Environment.objects.get(id=environment_id)
            self.auth_data = AuthDataParser(self.environment.name, self.country.name)
            self.client = Client(self.environment.b2b_rule_set_client)
        except Exception as e:
            traceback.print_exc()
            error_log(traceback.format_exc())
            raise e

    def request_data(self):
        try:
            self.execute()
        except Exception as e:
            traceback.print_exc()
            error_log(traceback.format_exc())
            raise e

    def get_result_data(self):
        try:
            return self.parse_result_data()
        except Exception as e:
            traceback.print_exc()
            error_log(traceback.format_exc())
            raise e

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def parse_result_data(self):
        pass
