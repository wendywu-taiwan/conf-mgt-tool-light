from RulesetComparer.date_model.json_builder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *


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
