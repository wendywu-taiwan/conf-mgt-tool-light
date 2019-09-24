import stat
from RulesetComparer.utils.fileManager import convert_file_size
from RulesetComparer.utils.timeUtil import *
from RulesetComparer.utils.logger import *


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
        self.size = str(size) + "bytes"
        # self.size = convert_file_size(size)

    def set_modification_time(self, modification_time):
        data_time = timestamp_to_date_time(modification_time)
        time_format = config.TIME_FORMAT.get("year_month_date_hour_minute_second")
        self.modification_time = date_time_to_time(data_time, time_format)

    def set_diff_result(self, diff_result):
        self.diff_result = diff_result

    def add_child_node_list(self, child_node):
        self.child_node_list.append(child_node)

    def sort_child_list(self):
        self.child_node_list.sort(key=lambda x: x.index, reverse=False)

    def get_node_json(self):
        return self.parse_node_json()

    def parse_node_json(self):
        json_obj = {KEY_NAME: self.name,
                    KEY_TYPE: self.type,
                    KEY_DIFF_RESULT: self.diff_result,
                    KEY_SIZE: self.size,
                    KEY_MODIFICATION_TIME: self.modification_time,
                    KEY_CHILD_NODES: self.parse_child_nodes_json()}
        return json_obj

    def parse_child_nodes_json(self):
        self.sort_child_list()
        json_list = list()
        for child_node in self.child_node_list:
            json_obj = {KEY_NAME: child_node.name,
                        KEY_TYPE: child_node.type,
                        KEY_DIFF_RESULT: child_node.diff_result,
                        KEY_SIZE: child_node.size,
                        KEY_MODIFICATION_TIME: child_node.modification_time,
                        KEY_CHILD_NODES: child_node.parse_child_nodes_json()}
            json_list.append(json_obj)
        return json_list
