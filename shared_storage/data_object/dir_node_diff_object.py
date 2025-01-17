from abc import abstractmethod

from RulesetComparer.utils.stringFilter import folder_filter
from common.data_object.diff_file_type_object import DiffFileTypeObject
from shared_storage.data_object.node_object import NodeObject
from shared_storage.data_object.dir_node_object import DirNodeObject, DirNodeLatestVersionObject, \
    DirNodeLatestVersionParentObject
from shared_storage.data_object.dir_entry_index_object import DirEntryIndexObject
from shared_storage.data_object.json_builder.file_detail_builder import FileDetailBuilder
from shared_storage.utils.file_manager import save_file_detail_json
from RulesetComparer.utils.logger import *
from shared_storage.properties.config import *


class DirNodeBaseObject:
    LOG_CLASS = "DirNodeBaseObject"

    def __init__(self, left_dir_connect_obj, right_dir_connect_obj, left_node, right_node,
                 left_filters=None, right_filters=None):
        self.left_node = left_node
        self.right_node = right_node
        self.left_dir_connect_obj = left_dir_connect_obj
        self.right_dir_connect_obj = right_dir_connect_obj
        self.left_entry_list = left_dir_connect_obj.get_path_list_dir(self.left_node.path)
        self.right_entry_list = right_dir_connect_obj.get_path_list_dir(self.right_node.path)
        self.root_key = self.left_dir_connect_obj.root_hash_key
        self.left_filters = left_filters
        self.right_filters = right_filters
        self.left_entry_map = {}
        self.right_entry_map = {}
        self.left_name_set = set()
        self.right_name_set = set()
        self.left_only = []
        self.right_only = []
        self.union = []

    def diff(self):
        try:
            self.parse_name_set()
            self.diff_to_list()
            self.parse_diff_nodes()
        except Exception as e:
            raise e

    @abstractmethod
    def parse_name_set(self):
        pass

    @staticmethod
    def parse_side_name_set(entry_list, entry_map, name_set):
        index = 0
        for entry in entry_list:
            name = entry.filename
            name_set.add(name)
            entry_index_obj = DirEntryIndexObject(entry, index)
            entry_map[name] = entry_index_obj
            index = index + 1

    @staticmethod
    def parse_filter_name_set(entry_list, entry_map, name_set, filters):
        index = 0
        for entry in entry_list:
            name = entry.filename

            if name not in filters:
                continue

            name_set.add(name)
            entry_index_obj = DirEntryIndexObject(entry, index)
            entry_map[name] = entry_index_obj
            index = index + 1

    def diff_to_list(self):
        # name only in left not in right
        self.left_only = list(set(self.left_name_set).difference(set(self.right_name_set)))
        # name only in right not in left
        self.right_only = list(set(self.right_name_set).difference(set(self.left_name_set)))
        # name in both set
        self.union = list(set(self.left_name_set) & set(self.right_name_set))

    def parse_diff_nodes(self):
        info_log(self.LOG_CLASS, "update_left_only_node, list:" + str(self.left_only))
        self.parse_environment_only_node(self.left_only, self.left_dir_connect_obj, self.left_entry_map,
                                         self.right_entry_map, self.left_node, self.right_node)
        info_log(self.LOG_CLASS, "update_right_only_node, list:" + str(self.right_only))
        self.parse_environment_only_node(self.right_only, self.right_dir_connect_obj, self.right_entry_map,
                                         self.left_entry_map, self.right_node, self.left_node)
        info_log(self.LOG_CLASS, "update_union_node, list:" + str(self.union))
        self.parse_union_node()

    @abstractmethod
    def parse_environment_only_node(self, name_list, dir_connect_obj, entry_map, opposite_entry_map,
                                    parent_node_add, parent_node_remove):
        pass

    @abstractmethod
    def parse_union_node(self):
        pass

    def parse_environment_only_child_node(self, name, entry_map, opposite_entry_map,
                                          parent_node_add, parent_node_remove):
        node_add = self.parse_node(name, entry_map, opposite_entry_map, parent_node_add, KEY_D_RESULT_ADD)
        node_remove = self.parse_node(name, entry_map, opposite_entry_map, parent_node_remove, KEY_D_RESULT_REMOVE)
        node_add.set_show_collapse()
        node_remove.set_show_collapse()
        self.update_node_hash_key(node_add, node_remove)
        return node_add, node_remove

    def parse_union_child_node(self, name):
        left_node = self.parse_node(name, self.left_entry_map, self.right_entry_map,
                                    self.left_node, KEY_D_RESULT_SAME)
        right_node = self.parse_node(name, self.right_entry_map, self.left_entry_map,
                                     self.right_node, KEY_D_RESULT_SAME)
        self.update_node_hash_key(left_node, right_node)
        return left_node, right_node

    def parse_node(self, name, entry_map, opposite_entry_map, parent_node, diff_result):
        entry_index_obj = entry_map.get(name)
        entry = entry_index_obj.entry
        index = entry_index_obj.index

        # handle order
        diff_index_obj = opposite_entry_map.get(name)
        if diff_index_obj is not None and diff_index_obj.index > index:
            index = diff_index_obj.index

        node = NodeObject(name, parent_node.environment, parent_node, index, entry.st_mode)
        node.set_size(entry.st_size)
        node.set_modification_time(entry.st_mtime)
        node.set_diff_result(diff_result)
        parent_node.add_child_node_list(node)
        info_log(self.LOG_CLASS,
                 "parse_node , index:" + str(node.index) + ", depth: " + str(node.depth) + ", path: " + node.path)
        return node

    def update_node_hash_key(self, left_node, right_node):
        node_hash_key = str(hash(left_node))
        left_node.set_node_hash_key(node_hash_key)
        right_node.set_node_hash_key(node_hash_key)
        return node_hash_key


class DirNodeDiffObject(DirNodeBaseObject):
    LOG_CLASS = "DirNodeDiffObject"

    def __init__(self, left_dir_connect_obj, right_dir_connect_obj, left_node, right_node,
                 left_filters=None, right_filters=None):
        DirNodeBaseObject.__init__(self, left_dir_connect_obj, right_dir_connect_obj, left_node, right_node,
                                   left_filters, right_filters)

    def diff(self):
        try:
            super().diff()
        except Exception as e:
            raise e

    def parse_name_set(self):
        self.parse_side_name_set(self.left_entry_list, self.left_entry_map, self.left_name_set)
        self.parse_side_name_set(self.right_entry_list, self.right_entry_map, self.right_name_set)

    # for other folder depth node
    def parse_environment_only_node(self, name_list, dir_connect_obj, entry_map, opposite_entry_map,
                                    parent_node_add, parent_node_remove):
        for name in name_list:
            node_add, node_remove = self.parse_environment_only_child_node(name, entry_map, opposite_entry_map,
                                                                           parent_node_add, parent_node_remove)
            # folder
            if node_add.type is KEY_FOLDER:
                child_node_obj = DirNodeObject(dir_connect_obj, node_add, node_remove)
                child_node_obj.parse_child_nodes()
            # file
            else:
                file_object = node_add.download_files(self.root_key, dir_connect_obj)
                json = FileDetailBuilder(file_object).get_data()
                save_file_detail_json(self.root_key, node_add.environment.name, node_add.node_hash_key, json)

    # for other folder depth node
    def parse_union_node(self):
        for name in self.union:
            left_node, right_node = self.parse_union_child_node(name)

            # folder
            if left_node.type is KEY_FOLDER:
                diff_obj = DirNodeDiffObject(self.left_dir_connect_obj, self.right_dir_connect_obj,
                                             left_node, right_node)
                diff_obj.diff()
            # file
            else:
                left_file_object = left_node.download_files(self.root_key, self.left_dir_connect_obj)
                right_file_object = right_node.download_files(self.root_key, self.right_dir_connect_obj)

                diff_file_type_object = DiffFileTypeObject(left_file_object, right_file_object,
                                                           self.root_key, left_node.node_hash_key)
                has_changes = diff_file_type_object.diff_file()

                if has_changes:
                    left_node.set_show_collapse()
                    right_node.set_show_collapse()
                    left_node.set_diff_result(KEY_DIFFERENT)
                    right_node.set_diff_result(KEY_DIFFERENT)


# for node that need to be filtered
class DirNodeDiffFilterObject(DirNodeDiffObject):
    LOG_CLASS = "DirNodeDiffFilterObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node, left_filters,
                 right_filters):
        try:
            DirNodeDiffObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node,
                                       left_filters, right_filters)
        except Exception as e:
            raise e

    def diff(self):
        try:
            super().diff()
        except Exception as e:
            raise e

    def parse_name_set(self):
        self.parse_filter_name_set(self.left_entry_list, self.left_entry_map, self.left_name_set,
                                   self.left_filters)
        self.parse_filter_name_set(self.right_entry_list, self.right_entry_map, self.right_name_set,
                                   self.right_filters)


# for node that is parent folder of latest version folder
class DirNodeDiffLatestVersionParentObject(DirNodeBaseObject):
    LOG_CLASS = "DirNodeDiffLatestVersionParentObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node,
                 left_filters=None, right_filters=None):
        try:
            DirNodeBaseObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node,
                                       left_filters, right_filters)
        except Exception as e:
            raise e

    def diff(self):
        try:
            super().diff()
        except Exception as e:
            raise e

    def parse_name_set(self):
        self.parse_side_name_set(self.left_entry_list, self.left_entry_map, self.left_name_set)
        self.parse_side_name_set(self.right_entry_list, self.right_entry_map, self.right_name_set)

    def parse_environment_only_node(self, name_list, dir_connect_obj, entry_map, opposite_entry_map,
                                    parent_node_add, parent_node_remove):
        for name in name_list:
            node_add, node_remove = self.parse_environment_only_child_node(name, entry_map, opposite_entry_map,
                                                                           parent_node_add, parent_node_remove)
            country_folder = self.left_dir_connect_obj.root_folder

            if folder_filter(country_folder, node_add.path, LATEST_VERSION_PARENT_FOLDER):
                child_node_obj = DirNodeLatestVersionObject(dir_connect_obj, node_add, node_remove)
                child_node_obj.parse_child_nodes()
            elif folder_filter(country_folder, node_add.path, LATEST_VERSION_GRAND_PARENT_FOLDER):
                child_node_obj = DirNodeLatestVersionParentObject(dir_connect_obj, node_add, node_remove)
                child_node_obj.parse_child_nodes()
            else:
                child_node_obj = DirNodeObject(dir_connect_obj, node_add, node_remove)
                child_node_obj.parse_child_nodes()

    def parse_union_node(self):
        for name in self.union:
            left_node, right_node = self.parse_union_child_node(name)
            country_folder = self.left_dir_connect_obj.root_folder

            if folder_filter(country_folder, left_node.path, LATEST_VERSION_PARENT_FOLDER):
                left_latest_version = self.left_dir_connect_obj.get_latest_version(left_node.path)
                right_latest_version = self.right_dir_connect_obj.get_latest_version(right_node.path)
                info_log(self.LOG_CLASS, "left_latest_version:" + str(left_latest_version))
                info_log(self.LOG_CLASS, "right_latest_version:" + str(right_latest_version))
                diff_obj = DirNodeDiffLatestVersionObject(self.left_dir_connect_obj, self.right_dir_connect_obj,
                                                          left_node, right_node,
                                                          [left_latest_version], [right_latest_version])
            elif folder_filter(country_folder, left_node.path, LATEST_VERSION_GRAND_PARENT_FOLDER):
                diff_obj = DirNodeDiffLatestVersionParentObject(self.left_dir_connect_obj, self.right_dir_connect_obj,
                                                                left_node, right_node)
            else:
                diff_obj = DirNodeDiffObject(self.left_dir_connect_obj, self.right_dir_connect_obj,
                                             left_node, right_node)
            diff_obj.diff()


# for node that is parent folder of latest version folder and need to be filtered
class DirNodeDiffFilteredLatestVersionParentObject(DirNodeDiffLatestVersionParentObject):
    LOG_CLASS = "DirNodeDiffFilteredLatestVersionParentObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node,
                 left_filters, right_filters):
        try:
            DirNodeDiffLatestVersionParentObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node,
                                                          right_node, left_filters, right_filters)
        except Exception as e:
            raise e

    def diff(self):
        try:
            super().diff()
        except Exception as e:
            raise e

    def parse_name_set(self):
        self.parse_filter_name_set(self.left_entry_list, self.left_entry_map, self.left_name_set,
                                   self.left_filters)
        self.parse_filter_name_set(self.right_entry_list, self.right_entry_map, self.right_name_set,
                                   self.right_filters)


# for node that is latest version folder
class DirNodeDiffLatestVersionObject(DirNodeDiffFilterObject):
    LOG_CLASS = "DirNodeDiffLastVersionObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node,
                 left_filters, right_filters):
        DirNodeDiffFilterObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj,
                                         left_node, right_node, left_filters, right_filters)

    def diff(self):
        try:
            super().parse_name_set()
            self.diff_latest_version_node()
        except Exception as e:
            raise e

    def diff_latest_version_node(self):
        left_node = self.parse_node(self.left_filters[0], self.left_entry_map, self.right_entry_map,
                                    self.left_node, KEY_D_RESULT_SAME)

        right_node = self.parse_node(self.right_filters[0], self.right_entry_map, self.left_entry_map,
                                     self.right_node, KEY_D_RESULT_SAME)

        self.update_node_hash_key(left_node, right_node)

        diff_obj = DirNodeDiffObject(self.left_dir_connect_obj, self.right_dir_connect_obj, left_node, right_node)
        diff_obj.diff()

    def parse_node(self, name, entry_map, opposite_entry_map, parent_node, diff_result):
        return super().parse_node(name, entry_map, opposite_entry_map, parent_node, diff_result)

    def update_node_hash_key(self, left_node, right_node):
        super().update_node_hash_key(left_node, right_node)
