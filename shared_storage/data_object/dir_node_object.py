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
        info_log(self.LOG_CLASS,
                 "node path: " + self.parent_node_add.path + ", depth: " + str(self.parent_node_add.depth))

    def parse_child_nodes(self):
        try:
            if self.parent_node_add.type is not KEY_FOLDER:
                return

            entry_list = self.dir_connect_obj.get_path_list_dir(self.parent_node_add.path)

            index = 0
            for entry in entry_list:
                self.parse_child_node(index, entry)
                index = index + 1
        except Exception as e:
            raise e

    def parse_child_node(self, index, entry):
        child_node_add = self.create_node(self.parent_node_add, index, entry, KEY_D_RESULT_ADD)
        child_node_remove = self.create_node(self.parent_node_remove, index, entry, KEY_D_RESULT_REMOVE)
        child_node_add.set_show_collapse()
        child_node_remove.set_show_collapse()
        self.update_node_hash_key(child_node_add, child_node_remove)

        next_depth_child_node_obj = DirNodeObject(self.dir_connect_obj, child_node_add, child_node_remove)
        next_depth_child_node_obj.parse_child_nodes()
        info_log(self.LOG_CLASS,
                 "parse_child_node , index:" + str(
                     child_node_add.index) + ", path: " + child_node_add.path + " , name: " + child_node_add.name)

    def create_node(self, parent_node, index, entry, diff_result):
        node = NodeObject(entry.filename, parent_node.environment, parent_node, index, entry.st_mode)
        node.set_size(entry.st_size)
        node.set_modification_time(entry.st_mtime)
        node.set_diff_result(diff_result)
        parent_node.add_child_node_list(node)
        return node

    def update_node_hash_key(self, left_node, right_node):
        node_hash_key = str(hash(left_node) + hash(right_node))
        left_node.set_node_hash_key(node_hash_key)
        right_node.set_node_hash_key(node_hash_key)
        return node_hash_key


class DirNodeLastVersionObject(DirNodeObject):
    LOG_CLASS = "DirNodeLastVersionObject"

    def __init__(self, dir_connect_obj, parent_node_add, parent_node_remove):
        DirNodeObject.__init__(self, dir_connect_obj, parent_node_add, parent_node_remove)

    def parse_child_nodes(self):
        try:
            index = 0
            last_version = self.dir_connect_obj.get_latest_version(self.parent_node_add.path)
            entry_list = self.dir_connect_obj.get_path_list_dir(self.parent_node_add.path)

            for entry in entry_list:
                name = entry.filename
                if last_version is not None and name != last_version:
                    continue

                self.parse_child_node(index, entry)
                index = index + 1
        except Exception as e:
            raise e

    def create_node(self, parent_node, index, entry, diff_result):
        return super().create_node(parent_node, index, entry, diff_result)

    def update_node_hash_key(self, left_node, right_node):
        return super().update_node_hash_key(left_node, right_node)
