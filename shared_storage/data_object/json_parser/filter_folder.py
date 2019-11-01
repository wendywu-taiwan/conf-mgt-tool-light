from shared_storage.properties.config import LATEST_VERSION_PARENT_FOLDER


class SelectToDownloadFilterFolderParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.environment_id = json_data.get("environment_id")
        except BaseException as e:
            raise e


class SelectToCompareFilterFolderParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.environment_id = json_data.get("environment_id")
            self.side = json_data.get("side")
        except BaseException as e:
            raise e


class SelectToDownloadFilterLatestVersionFolderParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.environment_id = json_data.get("environment_id")
            self.country_folder = json_data.get("country_folder")
            self.module_folder = json_data.get("module_folder")
            self.full_path = self.country_folder + "/" + self.module_folder
            self.git_full_path = "/" + self.country_folder + "/" + self.module_folder

            self.has_latest_version = self.parse_has_latest_version()
        except BaseException as e:
            raise e

    def parse_has_latest_version(self):
        if self.module_folder in LATEST_VERSION_PARENT_FOLDER:
            return True
        else:
            return False
