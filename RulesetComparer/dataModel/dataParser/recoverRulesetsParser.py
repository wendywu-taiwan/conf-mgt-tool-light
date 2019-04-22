from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.properties.dataKey import *
from RulesetComparer.utils.rulesetUtil import *


class RecoverRulesetsParser:
    def __init__(self, json_data):
        try:
            self.environment = Environment.objects.get(id=json_data[KEY_ENVIRONMENT_ID])
            self.country = Country.objects.get(id=json_data[KEY_COUNTRY_ID])
            self.select_folder_name = json_data[KEY_SELECT_FOLDER_NAME]
            self.created_rulesets = json_data[KEY_CREATED_RULESETS]
            self.updated_rulesets = json_data[KEY_UPDATED_RULESETS]
            self.deleted_rulesets = json_data[KEY_DELETED_RULESETS]
        except BaseException as e:
            raise e
