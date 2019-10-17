from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from shared_storage.utils.file_manager import load_folder_file_diff_json, load_file_diff_json


class BindFolderFileDiffResultBuilder(BaseBuilder):
    def __init__(self, root_key, node_key):
        try:
            self.root_json = load_folder_file_diff_json(root_key)
            self.file_json = load_file_diff_json(root_key, node_key)
            self.root_key = root_key

            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.file_json
        self.result_dict[KEY_LEFT_ENVIRONMENT] = self.root_json.get(KEY_LEFT_ENVIRONMENT)
        self.result_dict[KEY_RIGHT_ENVIRONMENT] = self.root_json.get(KEY_RIGHT_ENVIRONMENT)
        self.result_dict[KEY_LEFT_REGION] = self.root_json.get(KEY_LEFT_REGION)
        self.result_dict[KEY_RIGHT_REGION] = self.root_json.get(KEY_RIGHT_REGION)
        self.result_dict[KEY_LEFT_FOLDER] = self.root_json.get(KEY_LEFT_FOLDER)
        self.result_dict[KEY_RIGHT_FOLDER] = self.root_json.get(KEY_RIGHT_FOLDER)
        self.result_dict[KEY_ROOT_KEY] = self.root_key
