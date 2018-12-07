import traceback
from RulesetComparer.utils import fileManager
from RulesetComparer.properties import config
from RulesetComparer.utils.logger import *


class AuthDataParser:
    def __init__(self, environment):
        try:
            file_path = settings.BASE_DIR + config.get_file_path("auth_data")
            auth_data = fileManager.load_json_file(file_path)
            self.environment_data = auth_data[environment]
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def get_account(self):
        try:
            return self.environment_data["account"]
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def get_password(self):
        try:
            return self.environment_data["password"]
        except Exception:
            traceback.print_exc()
            logging.error(traceback.format_exc())
