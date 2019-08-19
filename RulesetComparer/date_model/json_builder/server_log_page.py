import re

from ConfigManageTool import settings
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleBaseBuilder
from RulesetComparer.utils.fileManager import *


class ServerLogPageBuilder(AdminConsoleBaseBuilder):
    def __init__(self, user, log_type):
        if log_type is None:
            self.log_type = DEFAULT_LOG_TYPE
        else:
            self.log_type = log_type
        self.log_file_name = ""
        self.file_content = ""
        AdminConsoleBaseBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[LOG_TYPE_KEY] = self.log_type
        self.result_dict[LOG_TYPE] = LOG_TYPE_FILE[self.log_type]
        self.result_dict[LOG_CONTENT] = self.parse_file_content

    def parse_file_content(self):
        log_dir = settings.BASE_DIR + get_file_path("server_log")
        log_file_name = LOG_TYPE_FILE[self.log_type]
        full_name = log_dir + "/" + log_file_name

        if is_file_exist(full_name) is False:
            info_log("views.admin_console_server_log_page", "init info message")
            warning_log("views.admin_console_server_log_page", "init warning message")
            error_log("init error message")

        file = load_file(full_name)
        file_secure = re.sub("password</ns0:name><ns0:value>[^<]+</ns0:value>",
                             "password</ns0:name><ns0:value>****</ns0:value>", file)
        return file_secure.split("\n")
