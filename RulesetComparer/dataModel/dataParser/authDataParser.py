import traceback
from RulesetComparer.utils import fileManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *


class AuthDataParser:
    ROOT_KEY = "ROOT"
    ACCOUNT_KEY = "account"
    PASSWORD_KEY = "password"

    def __init__(self, environment, country):
        try:
            file_path = settings.BASE_DIR + config.get_file_path("auth_data")
            auth_data = fileManager.load_json_file(file_path)
            environment_obj = auth_data[environment]
            if environment_obj.get(country) is not None:
                self.data = environment_obj[country]
            else:
                self.data = environment_obj[self.ROOT_KEY]
        except Exception as e:
            raise e

    def get_account(self):
        try:
            return self.data[self.ACCOUNT_KEY]
        except Exception as e:
            raise e

    def get_password(self):
        try:
            return self.data[self.PASSWORD_KEY]
        except Exception as e:
            raise e
