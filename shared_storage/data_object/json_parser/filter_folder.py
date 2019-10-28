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
