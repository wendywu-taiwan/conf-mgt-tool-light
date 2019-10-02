from RulesetComparer.utils import fileManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *


class AuthDataParser:
    ROOT_KEY = "ROOT"
    ACCOUNT_KEY = "account"
    PASSWORD_KEY = "password"
    KEY_AUTH_B2B_SERVICE = "B2BService"
    KEY_AUTH_FTP = "FTP"

    def __init__(self, auth_type, environment_name, country_name):
        try:
            file_path = settings.BASE_DIR + config.get_file_path("auth_data")
            auth_data = fileManager.load_json_file(file_path)
            environment_data = auth_data.get(environment_name)
            account_data = environment_data.get(auth_type)
            if account_data.get(country_name) is not None:
                self.data = account_data.get(country_name)
            elif account_data.get(self.ROOT_KEY) is not None:
                self.data = account_data.get(self.ROOT_KEY)
            else:
                self.data = {}
        except Exception as e:
            raise e

    def get_account(self):
        try:
            return self.data.get(self.ACCOUNT_KEY)
        except Exception as e:
            raise e

    def get_password(self):
        try:
            return self.data.get(self.PASSWORD_KEY)
        except Exception as e:
            raise e


class B2BServiceAuthDataParser(AuthDataParser):
    def __init__(self, environment, country):
        AuthDataParser.__init__(self, self.KEY_AUTH_B2B_SERVICE, environment, country)

    def get_account(self):
        return super().get_account()

    def get_password(self):
        return super().get_password()


class FTPAuthDataParser(AuthDataParser):
    def __init__(self, environment, region_name):
        AuthDataParser.__init__(self, self.KEY_AUTH_FTP, environment, region_name)

    def get_account(self):
        return super().get_account()

    def get_password(self):
        return super().get_password()
