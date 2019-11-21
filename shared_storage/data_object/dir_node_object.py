from paramiko import SFTPError

from shared_storage.data_object.json_builder.file_detail_builder import FileDetailBuilder
from shared_storage.data_object.node_object import NodeObject
from RulesetComparer.utils.logger import *
from shared_storage.utils.file_manager import save_file_detail_json


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
            entry_list = self.dir_connect_obj.get_path_list_dir(self.parent_node_add.path)
            index = 0
            for entry in entry_list:
                self.parse_child_node(index, entry)
                index = index + 1
        except NotADirectoryError:
            info_log(self.LOG_CLASS, "Not a directory: " + self.parent_node_add.path)
        except SFTPError:
            info_log(self.LOG_CLASS, "Not a directory: " + self.parent_node_add.path)
        except Exception as e:
            raise e

    def parse_child_node(self, index, entry):
        child_node_add, child_node_remove = self.get_child_node(index, entry)

        if child_node_add.type is KEY_FOLDER:
            next_depth_child_node_obj = DirNodeObject(self.dir_connect_obj, child_node_add, child_node_remove)
        else:
            next_depth_child_node_obj = FileNodeObject(self.dir_connect_obj, child_node_add, child_node_remove)

        next_depth_child_node_obj.parse_child_nodes()
        info_log(self.LOG_CLASS,
                 "parse_child_node , index:" + str(
                     child_node_add.index) + ", path: " + child_node_add.path + " , name: " + child_node_add.name)

    def get_child_node(self, index, entry):
        child_node_add = self.create_node(self.parent_node_add, index, entry, KEY_D_RESULT_ADD)
        child_node_remove = self.create_node(self.parent_node_remove, index, entry, KEY_D_RESULT_REMOVE)
        child_node_add.set_show_collapse()
        child_node_remove.set_show_collapse()

        node_hash_key = str(hash(child_node_add))
        child_node_add.set_node_hash_key(node_hash_key)
        child_node_remove.set_node_hash_key(node_hash_key)

        return child_node_add, child_node_remove

    @staticmethod
    def create_node(parent_node, index, entry, diff_result):
        node = NodeObject(entry.filename, parent_node.environment, parent_node, index, entry.st_mode)
        node.set_size(entry.st_size)
        node.set_modification_time(entry.st_mtime)
        node.set_diff_result(diff_result)
        parent_node.add_child_node_list(node)
        return node


class FileNodeObject(DirNodeObject):
    LOG_CLASS = "FileNodeObject"

    def __init__(self, dir_connect_obj, parent_node_add, parent_node_remove):
        DirNodeObject.__init__(self, dir_connect_obj, parent_node_add, parent_node_remove)

    def parse_child_nodes(self):
        try:
            file_object = self.parent_node_add.download_files(self.dir_connect_obj.root_hash_key, self.dir_connect_obj)
            json = FileDetailBuilder(file_object).get_data()
            save_file_detail_json(self.dir_connect_obj.root_hash_key,
                                  self.parent_node_add.environment.name,
                                  self.parent_node_add.node_hash_key, json)
        except Exception as e:
            raise e


class DirNodeLatestVersionParentObject(DirNodeObject):
    LOG_CLASS = "DirNodeLastVersionParentObject"

    def __init__(self, dir_connect_obj, parent_node_add, parent_node_remove):
        DirNodeObject.__init__(self, dir_connect_obj, parent_node_add, parent_node_remove)

    def parse_child_nodes(self):
        super().parse_child_nodes()

    def parse_child_node(self, index, entry):
        child_node_add, child_node_remove = self.get_child_node(index, entry)
        next_depth_child_node_obj = DirNodeLatestVersionObject(self.dir_connect_obj, child_node_add, child_node_remove)
        next_depth_child_node_obj.parse_child_nodes()


class DirNodeLatestVersionObject(DirNodeObject):
    LOG_CLASS = "DirNodeLastVersionObject"

    def __init__(self, dir_connect_obj, parent_node_add, parent_node_remove):
        DirNodeObject.__init__(self, dir_connect_obj, parent_node_add, parent_node_remove)

    def parse_child_nodes(self):
        try:
            index = 0
            latest_version = self.dir_connect_obj.get_latest_version(self.parent_node_add.path)
            entry_list = self.dir_connect_obj.get_path_list_dir(self.parent_node_add.path)

            for entry in entry_list:
                name = entry.filename
                if latest_version is not None and name != latest_version:
                    continue

                self.parse_child_node(index, entry)
                index = index + 1
        except Exception as e:
            raise e

    def parse_child_node(self, index, entry):
        child_node_add, child_node_remove = self.get_child_node(index, entry)
        next_depth_child_node_obj = DirNodeObject(self.dir_connect_obj, child_node_add, child_node_remove)
        next_depth_child_node_obj.parse_child_nodes()
