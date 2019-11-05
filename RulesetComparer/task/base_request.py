from zeep import Client
from abc import abstractmethod
from permission.models import Country, Environment, B2BServer, B2BService
from RulesetComparer.date_model.json_parser.auth_data import B2BServiceAuthDataParser


class BaseRequestTask:

    def __init__(self):
        self.success = True
        self.country = None
        self.environment = None
        self.auth_data = None
        self.client = None
        self.b2b_response_data = None
        self.result_data = None

    def parse_data(self, environment_id, country_id, b2b_service_name):
        try:
            self.country = Country.objects.get(id=country_id)
            self.environment = Environment.objects.get(id=environment_id)
            self.auth_data = B2BServiceAuthDataParser(self.environment.name, self.country.name)
            self.client = self.combine_client_url(b2b_service_name)
        except Exception as e:
            raise e

    def request_data(self):
        try:
            self.execute()
            self.parse_result_data()
        except Exception as e:
            raise e

    def get_result_data(self):
        return self.result_data

    def combine_client_url(self, service_name):
        try:
            server = B2BServer.objects.get(country=self.country.id, environment=self.environment.id)
        except B2BServer.DoesNotExist:
            raise Exception(
                "can not find server by environment: " + self.environment.name + " and country: " + self.country.name)
        try:
            service = B2BService.objects.get(name=service_name)
        except B2BService.DoesNotExist:
            raise Exception("can not find service by service name: " + service_name)

        url = server.client.url + service.url
        return Client(url)

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def parse_result_data(self):
        pass
