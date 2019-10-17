from abc import abstractmethod

from RulesetComparer.utils.fileManager import load_path_file
from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from shared_storage.properties.config import DIR_GIT_SHARE_STORAGE_ROOT, COMPARE_FILE_PATH
from shared_storage.utils.file_manager import load_folder_file_diff_json, load_file_detail_json, load_file_diff_json


class BindFileDetailBaseBuilder(BaseBuilder):
    LOG_CLASS = "BindFileDetailBaseBuilder"

    def __init__(self, side, root_key, node_key):
        try:
            self.side = side
            self.node_key = node_key
            self.root_key = root_key
            self.root_json = load_folder_file_diff_json(root_key)
            self.environment = None
            self.region = None
            self.folder = None
            self.file_name = None
            self.file_path = None
            self.modification_time = None
            self.node_json = None
            self.parse_root_info()
            self.parse_node_info()
            self.file_content = self.parse_content().splitlines()

            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def parse_root_info(self):
        if self.side == "left":
            self.environment = self.root_json.get(KEY_LEFT_ENVIRONMENT)
            self.region = self.root_json.get(KEY_LEFT_REGION)
            self.folder = self.root_json.get(KEY_LEFT_FOLDER)
        else:
            self.environment = self.root_json.get(KEY_RIGHT_ENVIRONMENT)
            self.region = self.root_json.get(KEY_RIGHT_REGION)
            self.folder = self.root_json.get(KEY_RIGHT_FOLDER)

    @abstractmethod
    def parse_node_info(self):
        pass

    def parse_content(self):
        environment_name = self.environment.get(KEY_NAME)
        file_name = self.node_json.get(KEY_FILE_NAME)

        if environment_name == GIT_NAME:
            file_path = DIR_GIT_SHARE_STORAGE_ROOT + self.node_json.get(KEY_FILE_PATH)
        else:
            file_path = COMPARE_FILE_PATH + "%s/%s/%s" % (self.root_key, self.environment.get(KEY_NAME), file_name)
        return load_path_file(file_path)

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENT] = self.environment
        self.result_dict[KEY_REGION] = self.region
        self.result_dict[KEY_FOLDER] = self.folder
        self.result_dict[KEY_ROOT_KEY] = self.root_key
        self.result_dict[KEY_FILE_NAME] = self.file_name
        self.result_dict[KEY_FILE_PATH] = self.file_path
        self.result_dict[KEY_MODIFICATION_TIME] = self.modification_time
        self.result_dict[KEY_DATA] = self.parse_content_json()

    def parse_content_json(self):
        result_list = list()
        index = 1
        for line in self.file_content:
            line_object = {KEY_INDEX: index, KEY_ROW: line}
            result_list.append(line_object)
            index = index + 1

        return result_list


class BindFileDetailBuilder(BindFileDetailBaseBuilder):
    LOG_CLASS = "BindFileDetailBuilder"

    def __init__(self, side, root_key, node_key):
        try:
            BindFileDetailBaseBuilder.__init__(self, side, root_key, node_key)
        except Exception as e:
            raise e

    def parse_node_info(self):
        self.node_json = load_file_detail_json(self.root_key, self.environment.get(KEY_NAME), self.node_key)
        self.file_name = self.node_json.get(KEY_FILE_NAME)
        self.file_path = self.node_json.get(KEY_FILE_PATH)
        self.modification_time = self.node_json.get(KEY_MODIFICATION_TIME)

    def __generate_data__(self):
        super().__generate_data__()


class BindFileSameDetailBuilder(BindFileDetailBaseBuilder):
    LOG_CLASS = "BindFileSameDetailBuilder"

    def __init__(self, side, root_key, node_key):
        try:
            BindFileDetailBaseBuilder.__init__(self, side, root_key, node_key)
        except Exception as e:
            raise e

    def parse_node_info(self):
        self.node_json = load_file_diff_json(self.root_key, self.node_key)
        self.file_name = self.node_json.get(KEY_FILE_NAME)

        if self.side == "left":
            self.file_path = self.node_json.get(KEY_LEFT_FILE)
            self.modification_time = self.node_json.get(KEY_LEFT_MODIFICATION_TIME)
        else:
            self.file_path = self.node_json.get(KEY_RIGHT_FILE)
            self.modification_time = self.node_json.get(KEY_RIGHT_MODIFICATION_TIME)

    def __generate_data__(self):
        super().__generate_data__()
