from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from permission.models import Country


class CountryBuilder(BaseBuilder):
    def __init__(self, country):
        try:
            self.country = country
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.country.id
        self.result_dict[KEY_NAME] = self.country.name
        self.result_dict[KEY_FULL_NAME] = self.country.full_name
        self.result_dict[KEY_ICON_FILE_NAME] = self.country.icon_file_name


class CountriesBuilder(BaseBuilder):
    def __init__(self, ids=None, countries=None):
        try:
            self.countries = []
            if ids is None:
                self.countries = countries
            else:
                for id in ids:
                    country = Country.objects.get(id=id)
                    self.countries.append(country)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.parse_countries()

    def parse_countries(self):
        array = []
        for country in self.countries:
            data = CountryBuilder(country).get_data()
            array.append(data)
        return array
