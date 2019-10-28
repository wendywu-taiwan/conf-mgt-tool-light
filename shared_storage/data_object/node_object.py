import stat

from RulesetComparer.utils.stringFilter import string_filter_array_keys
from RulesetComparer.utils.timeUtil import *
from RulesetComparer.utils.logger import *
from common.data_object.file_load_object import SharedStorageFileLoadObject


class NodeObject:
    LOG_CLASS = "NodeObject"

    def __init__(self, name, environment, parent_node, index, st_mode):
        self.id = None
        self.name = name
        self.environment = environment
        self.type = None
        self.depth = 0
        self.index = index
        self.parent_node = parent_node
        self.child_node_list = []
        self.path = None
        self.size = None
        self.modification_time = None
        self.diff_result = None
        self.st_mode = st_mode
        self.is_latest_version_node = False
        self.node_hash_key = None
        self.show_collapse = False
        self.parse_depth()
        self.parse_type()
        self.parse_path()
        self.parse_id()

    def parse_depth(self):
        if self.parent_node is None:
            self.depth = 0
        else:
            self.depth = self.parent_node.depth + 1

    def parse_type(self):
        if self.st_mode is None or stat.S_ISDIR(self.st_mode):
            self.type = KEY_FOLDER
        else:
            try:
                array = self.name.split(".")
                self.type = array[1]
            except IndexError:
                self.type = KEY_OTHERS

    def parse_id(self):
        self.id = self.name + "_" + str(self.depth) + "_" + str(self.index)

    def parse_path(self):
        if self.parent_node is None:
            self.path = "/" + self.name
        else:
            self.path = self.parent_node.path + "/" + self.name

    def set_size(self, size):
        self.size = str(size) + " bytes"

    def set_modification_time(self, modification_time):
        data_time = timestamp_to_date_time(modification_time)
        time_format = config.TIME_FORMAT.get("year_month_date_hour_minute_second")
        self.modification_time = date_time_to_time(data_time, time_format)

    def set_node_hash_key(self, node_hash_key):
        self.node_hash_key = str(node_hash_key)

    def set_diff_result(self, diff_result):
        self.diff_result = diff_result

    def set_show_collapse(self):
        self.show_collapse = True
        if self.parent_node is not None:
            self.parent_node.set_show_collapse()

    def add_child_node_list(self, child_node):
        self.child_node_list.append(child_node)

    def sort_child_list(self):
        self.child_node_list.sort(key=lambda x: x.index, reverse=False)

    # parse compare result json
    def parse_root_node_json(self):
        json_obj = {KEY_NAME: self.name,
                    KEY_TYPE: self.type,
                    KEY_DIFF_RESULT: KEY_D_RESULT_SAME,
                    KEY_SIZE: self.size,
                    KEY_DEPTH: self.depth,
                    KEY_INDEX: self.index,
                    KEY_SHOW_COLLAPSE: self.show_collapse,
                    KEY_MODIFICATION_TIME: self.modification_time,
                    KEY_CHILD_NODES: self.parse_child_nodes_json()}
        return json_obj

    # parse compare result json
    def parse_child_nodes_json(self):
        self.sort_child_list()
        json_list = list()
        for child_node in self.child_node_list:
            json_obj = {KEY_NAME: child_node.name,
                        KEY_TYPE: child_node.type,
                        KEY_DIFF_RESULT: child_node.diff_result,
                        KEY_SIZE: child_node.size,
                        KEY_DEPTH: child_node.depth,
                        KEY_INDEX: child_node.index,
                        KEY_COMPARE_HASH_KEY: child_node.node_hash_key,
                        KEY_MODIFICATION_TIME: child_node.modification_time}
            if len(child_node.child_node_list) > 0:
                json_obj[KEY_SHOW_COLLAPSE] = child_node.show_collapse
                json_obj[KEY_CHILD_NODES] = child_node.parse_child_nodes_json()
            json_list.append(json_obj)
        return json_list

    # parse compare result mail json
    def parse_mail_node_json(self, self_only_list, self_no_list, different_list):
        for child_node in self.child_node_list:
            if child_node.type is not KEY_FOLDER:
                data_object = {KEY_FILE_PATH: child_node.path,
                               KEY_TYPE: child_node.type,
                               KEY_DIFF_RESULT: child_node.diff_result,
                               KEY_COMPARE_HASH_KEY: child_node.node_hash_key}
                if child_node.diff_result is KEY_DIFFERENT:
                    different_list.append(data_object)
                elif child_node.diff_result is KEY_D_RESULT_ADD:
                    self_only_list.append(data_object)
                elif child_node.diff_result is KEY_D_RESULT_REMOVE:
                    self_no_list.append(data_object)

            child_node.parse_mail_node_json(self_only_list, self_no_list, different_list)

    def parse_filtered_files_list_json(self, connect_object, result_list, filtered_keys):
        for child_node in self.child_node_list:
            if child_node.type is not KEY_FOLDER and string_filter_array_keys(child_node.path, filtered_keys):
                data_object = {KEY_FILE_NAME: child_node.name,
                               KEY_FILE_PATH: child_node.path,
                               KEY_FILE_SIZE: child_node.size,
                               KEY_MODIFICATION_TIME: child_node.modification_time,
                               KEY_COMPARE_HASH_KEY: child_node.node_hash_key}
                result_list.append(data_object)
            child_node.parse_filtered_files_list_json(connect_object, result_list, filtered_keys)

    def parse_files_list_json(self):
        pass

    def download_files(self, root_key, connect_obj):
        root_key = root_key
        file_object = SharedStorageFileLoadObject(self.name, self.path, self.type, self.size, self.modification_time,
                                                  root_key, self.environment.name)
        file_object = connect_obj.get_file_contents(file_object)
        return file_object
