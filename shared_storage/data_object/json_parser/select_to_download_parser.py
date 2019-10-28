class SelectToDownloadFileListParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.environment_id = json_data.get("environment_id")
            self.folder_name = json_data.get("folder_name")
            self.module_name = json_data.get("module_name")
            self.only_latest_version = json_data.get("only_latest_version")
        except BaseException as e:
            raise e


class SelectToDownloadFilterResultParser(SelectToDownloadFileListParser):
    def __init__(self, json_data):
        try:
            SelectToDownloadFileListParser.__init__(self, json_data)
            self.filter_keys = json_data.get("filter_keys")
        except BaseException as e:
            raise e
