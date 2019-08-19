from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.properties.key import *


class DumpDataParser:
    def __init__(self, data):
        try:
            self.environment_array = data.get(KEY_ENVIRONMENTS)
            self.country_array = data.get(KEY_COUNTRIES)
            self.env_map = {}
            self.country_map = {}
        except Exception as e:
            raise e

    def parse_environment(self):
        for environment in self.environment_array:
            id = environment.get(KEY_ID)
            name = environment.get(KEY_NAME)
            self.env_map[id] = name

    def parse_country(self):
        for country in self.country_array:
            id = country.get(KEY_ID)
            name = country.get(KEY_NAME)
            self.country_map[id] = name

    def get_environment_name(self, id):
        return self.env_map[id]

    def get_country_name(self, id):
        return self.country_map[id]
