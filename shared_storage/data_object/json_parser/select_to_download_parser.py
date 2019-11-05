from RulesetComparer.properties.key import KEY_LAST_VERSION


class SelectToDownloadFileListParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.environment_id = json_data.get("environment_id")
            self.country_folder = json_data.get("country_folder")
            self.module_folder = json_data.get("module_folder")
            self.latest_version_folder = json_data.get("latest_version_folder")
            self.module_path = self.country_folder + "/" + self.module_folder
            self.only_latest_version = self.parse_only_last_version()
        except BaseException as e:
            raise e

    def parse_only_last_version(self):
        if self.latest_version_folder == KEY_LAST_VERSION:
            return True
        else:
            return False


class SelectToDownloadFilterResultParser(SelectToDownloadFileListParser):
    def __init__(self, json_data):
        try:
            SelectToDownloadFileListParser.__init__(self, json_data)
            self.filter_keys = json_data.get("filter_keys")
        except BaseException as e:
            raise e
