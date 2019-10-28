class SelectToDownloadFilterEnvironmentParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
        except BaseException as e:
            raise e


class SelectToCompareFilterEnvironmentParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.side = json_data.get("side")
        except BaseException as e:
            raise e
