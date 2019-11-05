class CompareSharedStorageFolderParser:

    def __init__(self, json_data):
        try:
            self.left_region_id = json_data.get("left_region_id")
            self.right_region_id = json_data.get("right_region_id")
            self.left_environment_id = json_data.get("left_environment_id")
            self.right_environment_id = json_data.get("right_environment_id")
            self.left_folder = json_data.get("left_folder")
            self.right_folder = json_data.get("right_folder")
            self.only_last_version = True
            self.apply_filter_folders = True
        except BaseException as e:
            raise e
