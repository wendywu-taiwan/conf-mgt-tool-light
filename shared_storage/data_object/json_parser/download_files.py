from permission.models import Environment


class DownloadFilesParser:

    def __init__(self, json_data):
        try:
            self.region_id = json_data.get("region_id")
            self.environment_id = json_data.get("environment_id")
            self.file_path_list = json_data.get("file_path_list")
            self.environment = Environment.objects.get(id=self.environment_id)
        except BaseException as e:
            raise e
