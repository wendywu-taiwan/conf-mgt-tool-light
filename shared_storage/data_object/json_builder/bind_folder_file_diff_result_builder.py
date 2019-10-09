import traceback
from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *


class BindFolderFileDiffResultBuilder(BaseBuilder):
    def __init__(self, root_json, file_json):
        try:
            self.left_environment = root_json.get(KEY_LEFT_ENVIRONMENT)
            self.right_environment = root_json.get(KEY_RIGHT_ENVIRONMENT)
            self.left_region = root_json.get(KEY_LEFT_REGION)
            self.right_region = root_json.get(KEY_RIGHT_REGION)
            self.left_folder = root_json.get(KEY_LEFT_FOLDER)
            self.right_folder = root_json.get(KEY_RIGHT_FOLDER)
            self.root_key = root_json.get(KEY_COMPARE_HASH_KEY)
            self.file_json = file_json

            BaseBuilder.__init__(self)
        except Exception as e:
            traceback.print_exc()
            raise e

    def __generate_data__(self):
        self.result_dict = self.file_json
        self.result_dict[KEY_LEFT_ENVIRONMENT] = self.left_environment
        self.result_dict[KEY_RIGHT_ENVIRONMENT] = self.right_environment
        self.result_dict[KEY_LEFT_REGION] = self.left_region
        self.result_dict[KEY_RIGHT_REGION] = self.right_region
        self.result_dict[KEY_LEFT_FOLDER] = self.left_folder
        self.result_dict[KEY_RIGHT_FOLDER] = self.right_folder
        self.result_dict[KEY_ROOT_KEY] = self.root_key
