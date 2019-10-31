class DownloadFilesParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.environment_id = json_data.get("environment_id")
            self.file_path_list = json_data.get("file_path_list")
        except BaseException as e:
            raise e
