from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties.dataKey import *
from RulesetComparer.models import Country, Environment
from RulesetComparer.date_model.json_builder.environment import EnvironmentBuilder
from RulesetComparer.date_model.json_builder.country import CountryBuilder


class RulesetDownloadPageBuilder(BaseBuilder):
    def __init__(self):
        self.countries = Country.objects.all()
        self.environments = Environment.objects.filter(active=1).values("id")
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[ENVIRONMENT_SELECT_COUNTRY] = self.parse_country()
        self.result_dict[ENVIRONMENT_SELECT_ENVIRONMENT] = self.parse_environment()

    def parse_country(self):
        country_list = []
        for country in self.countries:
            country_data = CountryBuilder(country).get_data()
            country_list.append(country_data)
        return country_list

    def parse_environment(self):
        environment_list = []
        for object in self.environments:
            environment_data = EnvironmentBuilder(id=object.get(KEY_ID)).get_data()
            environment_list.append(environment_data)
        return environment_list
