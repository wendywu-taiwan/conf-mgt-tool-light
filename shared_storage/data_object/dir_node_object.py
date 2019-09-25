import stat
import traceback
from shared_storage.data_object.node_object import NodeObject
from shared_storage.properties.config import *
from RulesetComparer.utils.logger import *


class DirNodeObject:
    LOG_CLASS = "DirNodeObject"

    def __init__(self, dir_connect_obj, parent_node_add, parent_node_remove):
        self.dir_connect_obj = dir_connect_obj
        self.parent_node_add = parent_node_add
        self.parent_node_remove = parent_node_remove
        self.depth = parent_node_add.depth + 1
        self.last_version = self.parse_last_version()
        info_log(self.LOG_CLASS,
                 "node path: " + self.parent_node_add.path + ", depth: " + str(self.parent_node_add.depth))

    def parse_last_version(self):
        if self.dir_connect_obj.only_last_version and self.depth == DEPTH_MODULE_VERSION:
            return self.dir_connect_obj.get_latest_version(self.parent_node_add.path)
        return None

    def parse_child_node(self):
        try:
            if self.parent_node_add.type is not KEY_FOLDER:
                return

            entry_list = self.dir_connect_obj.get_path_list_dir(self.parent_node_add.path)
            index = 0
            for entry in entry_list:
                name = entry.filename

                if self.last_version is not None and name != self.last_version:
                    continue

                child_node_add = NodeObject(name, self.parent_node_add.environment, self.parent_node_add, index,
                                            entry.st_mode)
                child_node_add.set_size(entry.st_size)
                child_node_add.set_modification_time(entry.st_mtime)
                child_node_add.set_diff_result(KEY_D_RESULT_ADD)
                self.parent_node_add.add_child_node_list(child_node_add)

                child_node_remove = NodeObject(name, self.parent_node_remove.environment, self.parent_node_remove,
                                               index, entry.st_mode)
                child_node_remove.set_size(entry.st_size)
                child_node_remove.set_modification_time(entry.st_mtime)
                child_node_remove.set_diff_result(KEY_D_RESULT_REMOVE)
                self.parent_node_remove.add_child_node_list(child_node_remove)

                next_depth_child_node_obj = DirNodeObject(self.dir_connect_obj, child_node_add, child_node_remove)
                info_log(self.LOG_CLASS,
                         "parse_child_node , index:" + str(
                             child_node_add.index) + ", path: " + child_node_add.path + " , name: " + child_node_add.name)

                next_depth_child_node_obj.parse_child_node()

                index = index + 1
        except Exception as e:
            traceback.print_exc()
            raise e
