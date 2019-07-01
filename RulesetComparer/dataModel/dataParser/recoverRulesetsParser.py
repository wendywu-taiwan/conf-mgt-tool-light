from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.properties.dataKey import *
from RulesetComparer.utils.rulesetUtil import *


class RecoverRulesetsParser:
    def __init__(self, json_data):
        try:
            self.source_environment = Environment.objects.get(name=BACKUP_ENVIRONMENT_NAME)
            self.target_environment = Environment.objects.get(id=json_data.get(KEY_TARGET_ENV_ID))
            self.country = Country.objects.get(id=json_data[KEY_COUNTRY_ID])
            self.backup_key = json_data[KEY_BACKUP_KEY]
            self.applied_to_server_rulesets = json_data[KEY_APPLIED_RULESETS]
        except BaseException as e:
            raise e
