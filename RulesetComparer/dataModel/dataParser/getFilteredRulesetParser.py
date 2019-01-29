import traceback
from RulesetComparer.utils.logger import *
from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment, Country


class GetFilteredRulesetParser:
    JSON_KEY_ENV_ID = "environment_id"
    JSON_KEY_COUNTRY_ID = "country_id"
    JSON_KEY_FILTER_KEYS = "filter_keys"

    def __init__(self, json_data):
        try:
            self.environment = Environment.objects.get(id=json_data[self.JSON_KEY_ENV_ID])
            self.country = Country.objects.get(id=json_data[self.JSON_KEY_COUNTRY_ID])
            self.filter_keys = json_data[self.JSON_KEY_FILTER_KEYS]
            self.is_git = self.is_git_env()
        except BaseException as e:
            traceback.print_exc()
            error_log(traceback.format_exc())
            raise e

    def is_git_env(self):
        try:
            if self.environment.name == GIT["environment_name"]:
                return True
            else:
                return False
        except BaseException:
            traceback.print_exc()
            error_log(traceback.format_exc())
            