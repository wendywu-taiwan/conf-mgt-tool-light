from common.data_object.json_builder.base import BaseBuilder


class JobSuccessContentBuilder(BaseBuilder):

    def __init__(self, task_name):
        self.task_name = task_name
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict["task_name"] = self.task_name

    def generate_normal_files_data(self, delete_files):
        message = "removed files success"

        if delete_files is None or len(delete_files) == 0:
            result_file_obj = {"data_title": "No deleted files"}
        else:
            files_count = len(delete_files)
            result_file_obj = {"data_title": "Deleted files : " + str(files_count),
                               "content": delete_files}
        data_array = [result_file_obj]
        self.result_dict["message"] = message
        self.result_dict["data"] = data_array

    def generate_clear_rulesets_files_data(self, delete_rulesets, delete_zip_files):
        message = "clear zip files and ruleset files success"

        if delete_rulesets is None or len(delete_rulesets) == 0:
            ruleset_file_obj = {"data_title": "No deleted ruleset"}
        else:
            ruleset_file_obj = {"data_title": "Deleted Ruleset Files",
                                "content": delete_rulesets}

        if delete_zip_files is None or len(delete_zip_files) == 0:
            zip_file_obj = {"data_title": "No deleted zip files"}
        else:
            zip_file_obj = {"data_title": "Deleted Zip Files",
                            "content": delete_zip_files}

        data_array = [ruleset_file_obj,
                      zip_file_obj]

        self.result_dict["message"] = message
        self.result_dict["data"] = data_array

    def get_data(self):
        return self.result_dict
