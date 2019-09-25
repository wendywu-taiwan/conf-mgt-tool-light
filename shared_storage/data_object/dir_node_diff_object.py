import traceback

from common.data_object.file_load_object import SharedStorageFileLoadObject
from common.data_object.diff_file_type_object import DiffFileTypeObject
from shared_storage.data_object.node_object import NodeObject
from shared_storage.data_object.dir_node_object import DirNodeObject
from shared_storage.data_object.dir_entry_index_object import DirEntryIndexObject
from RulesetComparer.utils.logger import *
from shared_storage.properties.config import *


class DirNodeDiffObject:
    LOG_CLASS = "DirNodeDiffObject"

    def __init__(self, left_dir_connect_obj, right_dir_connect_obj, left_node, right_node):
        self.depth = left_node.depth
        self.index = left_node.index
        self.left_node = left_node
        self.right_node = right_node
        self.left_dir_connect_obj = left_dir_connect_obj
        self.right_dir_connect_obj = right_dir_connect_obj
        self.left_entry_map = {}
        self.right_entry_map = {}
        self.left_name_set = set()
        self.right_name_set = set()
        self.left_only = []
        self.right_only = []
        self.union = []

    def diff(self):
        try:
            left_entry_list = self.left_dir_connect_obj.get_path_list_dir(self.left_node.path)
            right_entry_list = self.right_dir_connect_obj.get_path_list_dir(self.right_node.path)
            self.parse_name_set(left_entry_list, self.left_entry_map, self.left_name_set)
            self.parse_name_set(right_entry_list, self.right_entry_map, self.right_name_set)
            self.diff_to_list()
            self.parse_left_only_node()
            self.parse_right_only_node()
            self.parse_union_node()
        except Exception as e:
            traceback.print_exc()
            raise e

    @staticmethod
    def parse_name_set(entry_list, entry_map, name_set):
        index = 0
        for entry in entry_list:
            name = entry.filename
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

    def parse_left_only_node(self):
        info_log(self.LOG_CLASS, "update_left_only_node, list:" + str(self.left_only))
        for name in self.left_only:
            self.parse_environment_only_node(name, self.left_dir_connect_obj, self.left_entry_map,
                                             self.right_entry_map, self.left_node, self.right_node)

    def parse_right_only_node(self):
        info_log(self.LOG_CLASS, "update_right_only_node, list:" + str(self.right_only))
        for name in self.right_only:
            self.parse_environment_only_node(name, self.right_dir_connect_obj, self.right_entry_map,
                                             self.left_entry_map, self.right_node, self.left_node)

    def parse_environment_only_node(self, name, dir_connect_obj, entry_map, opposite_entry_map, parent_node_add,
                                    parent_node_remove):
        node_add = self.parse_node(name, entry_map, opposite_entry_map, parent_node_add)
        node_add.set_diff_result(KEY_D_RESULT_ADD)

        node_remove = self.parse_node(name, entry_map, opposite_entry_map, parent_node_remove)
        node_remove.set_diff_result(KEY_D_RESULT_REMOVE)

        if node_add.type is KEY_FOLDER:
            child_node_obj = DirNodeObject(dir_connect_obj, node_add, node_remove)
            child_node_obj.parse_child_node()

    def parse_union_node(self):
        info_log(self.LOG_CLASS, "update_union_node, list:" + str(self.union))

        current_depth = self.left_node.depth + 1
        only_last_version = self.left_dir_connect_obj.only_last_version

        if current_depth == DEPTH_MODULE_FOLDER and only_last_version:
            self.apply_latest_version_diff()
        else:
            for name in self.union:
                left_node = self.parse_node(name, self.left_entry_map, self.right_entry_map, self.left_node)
                left_node.set_diff_result(KEY_D_RESULT_SAME)

                right_node = self.parse_node(name, self.right_entry_map, self.left_entry_map, self.right_node)
                right_node.set_diff_result(KEY_D_RESULT_SAME)

                # diff folder
                if left_node.type is KEY_FOLDER:
                    diff_obj = DirNodeDiffObject(self.left_dir_connect_obj, self.right_dir_connect_obj, left_node,
                                                 right_node)
                    diff_obj.diff()
                # diff file
                else:
                    left_file_object = SharedStorageFileLoadObject(left_node.name, left_node.path, left_node.type,
                                                                   left_node.size)
                    right_file_object = SharedStorageFileLoadObject(right_node.name, right_node.path, right_node.type,
                                                                    right_node.size)
                    left_file_object = self.left_dir_connect_obj.get_file_contents(left_file_object)
                    right_file_object = self.right_dir_connect_obj.get_file_contents(right_file_object)
                    diff_file_type_object = DiffFileTypeObject(left_file_object, right_file_object,
                                                               self.left_dir_connect_obj.compare_key)
                    has_changes = diff_file_type_object.diff_file()

                    if has_changes:
                        left_node.set_diff_result(KEY_D_RESULT_DIFFERENT)
                        right_node.set_diff_result(KEY_D_RESULT_DIFFERENT)

    def apply_latest_version_diff(self):
        for name in self.union:
            left_node = self.parse_node(name, self.left_entry_map, self.right_entry_map, self.left_node)
            right_node = self.parse_node(name, self.right_entry_map, self.left_entry_map, self.right_node)

            left_node.set_diff_result(KEY_D_RESULT_SAME)
            right_node.set_diff_result(KEY_D_RESULT_SAME)

            left_last_version = self.left_dir_connect_obj.get_latest_version(left_node.path)
            right_last_version = self.right_dir_connect_obj.get_latest_version(right_node.path)
            info_log(self.LOG_CLASS, "left_last_version:" + str(left_last_version))
            info_log(self.LOG_CLASS, "right_last_version:" + str(right_last_version))
            diff_obj = DirNodeDiffLastVersionObject(self.left_dir_connect_obj,
                                                    self.right_dir_connect_obj,
                                                    left_node, right_node,
                                                    [left_last_version], [right_last_version])
            diff_obj.diff()

    def parse_node(self, name, entry_map, opposite_entry_map, parent_node):
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
        parent_node.add_child_node_list(node)
        info_log(self.LOG_CLASS,
                 "parse_node , index:" + str(node.index) + ", depth: " + str(node.depth) + ", path: " + node.path)
        return node


class DirNodeDiffFilterObject(DirNodeDiffObject):
    LOG_CLASS = "DirNodeDiffFilterObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node, left_filters,
                 right_filters):
        try:
            DirNodeDiffObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node)
            self.left_filters = left_filters
            self.right_filters = right_filters
        except Exception as e:
            traceback.print_exc()
            raise e

    def diff(self):
        try:
            left_entry_list = self.left_dir_connect_obj.get_path_list_dir(self.left_node.path)
            right_entry_list = self.right_dir_connect_obj.get_path_list_dir(self.right_node.path)
            self.parse_filter_node_object(left_entry_list, self.left_entry_map, self.left_name_set,
                                          self.left_filters)
            self.parse_filter_node_object(right_entry_list, self.right_entry_map, self.right_name_set,
                                          self.right_filters)
            self.diff_to_list()
            self.parse_left_only_node()
            self.parse_right_only_node()
            self.parse_union_node()
        except Exception as e:
            traceback.print_exc()
            raise e

    def parse_filter_node_object(self, entry_list, entry_map, name_set, filters):
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
        super().diff_to_list()

    def parse_left_only_node(self):
        super().parse_left_only_node()

    def parse_right_only_node(self):
        super().parse_right_only_node()

    def parse_union_node(self):
        super().parse_union_node()

    def parse_node(self, name, entry_map, opposite_entry_map, parent_node):
        return super().parse_node(name, entry_map, opposite_entry_map, parent_node)


class DirNodeDiffLastVersionObject(DirNodeDiffFilterObject):
    LOG_CLASS = "DirNodeDiffLastVersionObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node, left_filters,
                 right_filters):
        try:
            DirNodeDiffFilterObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj,
                                             left_node, right_node, left_filters, right_filters)
        except Exception as e:
            traceback.print_exc()
            raise e

    def diff(self):
        try:
            left_entry_list = self.left_dir_connect_obj.get_path_list_dir(self.left_node.path)
            right_entry_list = self.right_dir_connect_obj.get_path_list_dir(self.right_node.path)
            self.parse_filter_node_object(left_entry_list, self.left_entry_map, self.left_name_set,
                                          self.left_filters)
            self.parse_filter_node_object(right_entry_list, self.right_entry_map, self.right_name_set,
                                          self.right_filters)
            self.diff_last_version_node()
        except Exception as e:
            traceback.print_exc()
            raise e

    def parse_filter_node_object(self, entry_list, entry_map, name_set, filters):
        super().parse_filter_node_object(entry_list, entry_map, name_set, filters)

    def diff_last_version_node(self):
        left_node = self.parse_node(self.left_filters[0], self.left_entry_map, self.right_entry_map, self.left_node)
        left_node.set_diff_result(KEY_D_RESULT_SAME)

        right_node = self.parse_node(self.right_filters[0], self.right_entry_map, self.left_entry_map, self.right_node)
        right_node.set_diff_result(KEY_D_RESULT_SAME)

        diff_obj = DirNodeDiffObject(self.left_dir_connect_obj, self.right_dir_connect_obj, left_node, right_node)
        diff_obj.diff()

    def parse_node(self, name, entry_map, opposite_entry_map, parent_node):
        return super().parse_node(name, entry_map, opposite_entry_map, parent_node)
