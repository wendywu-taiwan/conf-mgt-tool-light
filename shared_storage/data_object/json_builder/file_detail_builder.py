from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.utils.fileManager import load_path_file
from RulesetComparer.utils.logger import info_log
from shared_storage.properties.config import COMPARE_FILE_PATH, DIR_GIT_SHARE_STORAGE_ROOT
from shared_storage.utils.file_manager import load_folder_file_diff_json, load_file_detail_json, load_file_diff_json


class FileDetailBuilder(BaseBuilder):
    def __init__(self, file_object):
        try:
            self.file_object = file_object
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_FILE_NAME] = self.file_object.file_name
        self.result_dict[KEY_FILE_PATH] = self.file_object.file_path
        self.result_dict[KEY_FILE_SIZE] = self.file_object.file_size
        self.result_dict[KEY_MODIFICATION_TIME] = self.file_object.modification_time


class BindFileDetailBuilder(BaseBuilder):
    LOG_CLASS = "BindFileDetailBuilder"

    def __init__(self, side, root_key, node_key):
        try:
            self.root_key = root_key

            root_json = load_folder_file_diff_json(root_key)

            if side == "left":
                self.environment = root_json.get(KEY_LEFT_ENVIRONMENT)
                self.region = root_json.get(KEY_LEFT_REGION)
                self.folder = root_json.get(KEY_LEFT_FOLDER)
            else:
                self.environment = root_json.get(KEY_RIGHT_ENVIRONMENT)
                self.region = root_json.get(KEY_RIGHT_REGION)
                self.folder = root_json.get(KEY_RIGHT_FOLDER)

            self.node_json = load_file_detail_json(root_key, self.environment.get(KEY_NAME), node_key)
            self.file_content = self.parse_content().splitlines()

            info_log(self.LOG_CLASS,
                     "root_key : " + root_key + ", node_key: " + node_key + ", file name :" + self.node_json.get(
                         KEY_FILE_NAME))

            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.node_json
        self.result_dict[KEY_ENVIRONMENT] = self.environment
        self.result_dict[KEY_REGION] = self.region
        self.result_dict[KEY_FOLDER] = self.folder
        self.result_dict[KEY_ROOT_KEY] = self.root_key
        self.result_dict[KEY_DATA] = self.parse_content_json()

    def parse_content(self):
        environment_name = self.environment.get(KEY_NAME)
        file_name = self.node_json.get(KEY_FILE_NAME)

        if environment_name == GIT_NAME:
            file_path = DIR_GIT_SHARE_STORAGE_ROOT + self.node_json.get(KEY_FILE_PATH)
        else:
            file_path = COMPARE_FILE_PATH + "%s/%s/%s" % (self.root_key, self.environment.get(KEY_NAME), file_name)
        return load_path_file(file_path)

    def parse_content_json(self):
        result_list = list()
        index = 1
        for line in self.file_content:
            line_object = {KEY_INDEX: index, KEY_ROW: line}
            result_list.append(line_object)
            index = index + 1

        return result_list


class BindFileSameDetailBuilder(BaseBuilder):
    LOG_CLASS = "BindFileSameDetailBuilder"

    def __init__(self, side, root_key, node_key):
        try:
            self.root_key = root_key

            root_json = load_folder_file_diff_json(root_key)
            self.node_json = load_file_diff_json(root_key, node_key)

            if side == "left":
                self.environment = root_json.get(KEY_LEFT_ENVIRONMENT)
                self.region = root_json.get(KEY_LEFT_REGION)
                self.folder = root_json.get(KEY_LEFT_FOLDER)
                self.file_name = self.node_json.get(KEY_FILE_NAME)
                self.file_path = self.node_json.get(KEY_LEFT_FILE)
                self.modification_time = self.node_json.get(KEY_LEFT_MODIFICATION_TIME)
            else:
                self.environment = root_json.get(KEY_RIGHT_ENVIRONMENT)
                self.region = root_json.get(KEY_RIGHT_REGION)
                self.folder = root_json.get(KEY_RIGHT_FOLDER)
                self.file_name = self.node_json.get(KEY_FILE_NAME)
                self.file_path = self.node_json.get(KEY_RIGHT_FILE)
                self.modification_time = self.node_json.get(KEY_RIGHT_MODIFICATION_TIME)

            self.file_content = self.parse_content().splitlines()

            info_log(self.LOG_CLASS,
                     "root_key : " + root_key + ", node_key: " + node_key + ", file name :" + self.file_name)

            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENT] = self.environment
        self.result_dict[KEY_REGION] = self.region
        self.result_dict[KEY_FOLDER] = self.folder
        self.result_dict[KEY_ROOT_KEY] = self.root_key
        self.result_dict[KEY_FILE_NAME] = self.file_name
        self.result_dict[KEY_FILE_PATH] = self.file_path
        self.result_dict[KEY_MODIFICATION_TIME] = self.modification_time
        self.result_dict[KEY_DATA] = self.parse_content_json()

    def parse_content(self):
        environment_name = self.environment.get(KEY_NAME)
        file_name = self.node_json.get(KEY_FILE_NAME)

        if environment_name == GIT_NAME:
            file_path = DIR_GIT_SHARE_STORAGE_ROOT + self.file_path
        else:
            file_path = COMPARE_FILE_PATH + "%s/%s/%s" % (self.root_key, self.environment.get(KEY_NAME), file_name)
        return load_path_file(file_path)

    def parse_content_json(self):
        result_list = list()
        index = 1
        for line in self.file_content:
            line_object = {KEY_INDEX: index, KEY_ROW: line}
            result_list.append(line_object)
            index = index + 1

        return result_list
