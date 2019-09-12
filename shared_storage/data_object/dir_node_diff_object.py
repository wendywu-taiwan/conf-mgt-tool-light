import traceback
import stat
from shared_storage.data_object.node_object import NodeObject
from shared_storage.data_object.dir_node_object import DirNodeObject
from RulesetComparer.utils.logger import *
from shared_storage.properties.config import *


class DirNodeDiffObject:
    LOG_CLASS = "DirNodeDiffObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node):
        try:
            self.depth = left_node.depth
            self.index = left_node.index
            self.left_node = left_node
            self.right_node = right_node
            self.left_ftp_connect_obj = left_ftp_connect_obj
            self.right_ftp_connect_obj = right_ftp_connect_obj
            self.left_store_map = {}
            self.right_store_map = {}
            self.left_name_set = set()
            self.right_name_set = set()
            self.left_only = []
            self.right_only = []
            self.union = []
        except Exception as e:
            traceback.print_exc()
            raise e

    def diff(self):
        try:
            left_entry_list = self.left_ftp_connect_obj.get_path_list_dir(self.left_node.path)
            right_entry_list = self.right_ftp_connect_obj.get_path_list_dir(self.right_node.path)
            self.parse_node_object(left_entry_list, self.left_name_set)
            self.parse_node_object(right_entry_list, self.right_name_set)
            self.diff_to_list()
            self.update_left_only_node()
            self.update_right_only_node()
            self.update_union_node()
        except Exception as e:
            traceback.print_exc()
            raise e

    def parse_node_object(self, entry_list, name_set):
        index = 0
        for entry in entry_list:
            name = entry.filename
            if any([name in i for i in name_set]):
                continue

            st_mode = stat.S_ISDIR(entry.st_mode)
            self.parse_node(index, name, entry.st_size, entry.st_mtime,
                            self.left_node, self.left_store_map, st_mode)

            self.parse_node(index, name, entry.st_size, entry.st_mtime,
                            self.right_node, self.right_store_map, st_mode)

            name_set.add(name)
            index = index + 1

    def parse_node(self, index, name, size, time, parent_node, node_map, st_mode):
        node = NodeObject(name, parent_node.environment, parent_node, index, st_mode)
        node.set_size(size)
        node.set_modification_time(time)
        parent_node.add_child_node_list(node)
        info_log(self.LOG_CLASS, "parent_node add node, parent name: "+parent_node.name)

        info_log(self.LOG_CLASS, "parse_node , index:" + str(
                     node.index) + ", depth: " + str(node.depth) + ", path: " + node.path + " , name: " + node.name)
        node_map[node.name] = node

    def diff_to_list(self):
        # name only in left not in right
        self.left_only = list(set(self.left_name_set).difference(set(self.right_name_set)))
        # name only in right not in left
        self.right_only = list(set(self.right_name_set).difference(set(self.left_name_set)))
        # name in both set
        self.union = list(set(self.left_name_set) & set(self.right_name_set))

    def update_left_only_node(self):
        info_log(self.LOG_CLASS, "update_left_only_node, list:" + str(self.left_only))
        for name in self.left_only:
            self.update_environment_only_node(self.left_ftp_connect_obj, self.left_store_map, self.right_store_map,
                                              name)

    def update_right_only_node(self):
        info_log(self.LOG_CLASS, "update_right_only_node, list:" + str(self.right_only))
        for name in self.right_only:
            self.update_environment_only_node(self.right_ftp_connect_obj, self.right_store_map, self.left_store_map,
                                              name)

    def update_environment_only_node(self, ftp_connect_obj, node_add_map, node_remove_map, name):
        node_add = node_add_map.get(name)
        node_add.set_diff_result(KEY_D_RESULT_ADD)

        node_remove = node_remove_map.get(name)
        node_remove.set_diff_result(KEY_D_RESULT_REMOVE)

        if node_add.type is KEY_FOLDER:
            child_node_obj = DirNodeObject(ftp_connect_obj, node_add, node_remove)
            child_node_obj.parse_child_node()

    def update_union_node(self):
        info_log(self.LOG_CLASS, "update_union_node, list:" + str(self.union))

        for name in self.union:
            left_node = self.left_store_map.get(name)
            right_node = self.right_store_map.get(name)

            right_node.set_diff_result(KEY_D_RESULT_SAME)
            left_node.set_diff_result(KEY_D_RESULT_SAME)

            depth = left_node.depth
            only_last_version = self.left_ftp_connect_obj.only_last_version
            if depth == DEPTH_MODULE_FOLDER and only_last_version:
                left_last_version = self.left_ftp_connect_obj.get_latest_version(left_node.path)
                info_log(self.LOG_CLASS, "left_last_version:" + str(left_last_version))
                right_last_version = self.right_ftp_connect_obj.get_latest_version(right_node.path)
                info_log(self.LOG_CLASS, "right_last_version:" + str(right_last_version))
                diff_obj = DirNodeDiffLastVersionObject(self.left_ftp_connect_obj,
                                                        self.right_ftp_connect_obj,
                                                        left_node, right_node,
                                                        [left_last_version], [right_last_version])
                diff_obj.diff()
            else:
                if left_node.type is not KEY_FOLDER:
                    diff_obj = None
                    info_log(self.LOG_CLASS, "diff file, name :" + left_node.name)
                    pass
                else:
                    diff_obj = DirNodeDiffObject(self.left_ftp_connect_obj, self.right_ftp_connect_obj,
                                                 left_node, right_node)
                    diff_obj.diff()


class DirNodeDiffFilterObject(DirNodeDiffObject):
    LOG_CLASS = "DirNodeDiffFilterObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node, left_filters, right_filters):
        try:
            DirNodeDiffObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node)
            self.left_filters = left_filters
            self.right_filters = right_filters
        except Exception as e:
            traceback.print_exc()
            raise e

    def diff(self):
        try:
            left_entry_list = self.left_ftp_connect_obj.get_path_list_dir(self.left_node.path)
            right_entry_list = self.right_ftp_connect_obj.get_path_list_dir(self.right_node.path)
            self.parse_filter_node_object(left_entry_list, self.left_name_set, self.left_filters)
            self.parse_filter_node_object(right_entry_list, self.right_name_set, self.right_filters)
            self.diff_to_list()
            self.update_left_only_node()
            self.update_right_only_node()
            self.update_union_node()
        except Exception as e:
            traceback.print_exc()
            raise e

    def parse_filter_node_object(self, entry_list, name_set, filters):
        index = 0
        for entry in entry_list:
            name = entry.filename
            if any([name in i for i in name_set]):
                continue

            if name not in filters:
                continue

            self.parse_node(index, name, entry.st_size, entry.st_mtime,
                            self.left_node, self.left_store_map, entry.st_mode)

            self.parse_node(index, name, entry.st_size, entry.st_mtime,
                            self.right_node, self.right_store_map, entry.st_mode)

            name_set.add(name)
            index = index + 1

    def parse_node(self, index, name, size, time, parent_node, node_map, st_mode):
        super().parse_node(index, name, size, time, parent_node, node_map, st_mode)

    def diff_to_list(self):
        super().diff_to_list()

    def update_left_only_node(self):
        super().update_left_only_node()

    def update_right_only_node(self):
        super().update_right_only_node()

    def update_environment_only_node(self, ftp_connect_obj, node_add_map, node_remove_map, name):
        super().update_environment_only_node(ftp_connect_obj, node_add_map, node_remove_map, name)

    def update_union_node(self):
        super().update_union_node()


class DirNodeDiffLastVersionObject(DirNodeDiffFilterObject):
    LOG_CLASS = "DirNodeDiffLastVersionObject"

    def __init__(self, left_ftp_connect_obj, right_ftp_connect_obj, left_node, right_node, left_filters, right_filters):
        try:
            DirNodeDiffFilterObject.__init__(self, left_ftp_connect_obj, right_ftp_connect_obj,
                                             left_node, right_node, left_filters, right_filters)
        except Exception as e:
            traceback.print_exc()
            raise e

    def diff(self):
        try:
            left_entry_list = self.left_ftp_connect_obj.get_path_list_dir(self.left_node.path)
            right_entry_list = self.right_ftp_connect_obj.get_path_list_dir(self.right_node.path)
            self.parse_filter_node_object(left_entry_list, self.left_name_set, self.left_filters)
            self.parse_filter_node_object(right_entry_list, self.right_name_set, self.right_filters)
            self.diff_last_version_node()
        except Exception as e:
            traceback.print_exc()
            raise e

    def parse_filter_node_object(self, entry_list, name_set, filters):
        super().parse_filter_node_object(entry_list, name_set, filters)

    def diff_last_version_node(self):
        left_node = self.left_store_map.get(self.left_filters[0])
        right_node = self.right_store_map.get(self.right_filters[0])

        right_node.set_diff_result(KEY_D_RESULT_SAME)
        left_node.set_diff_result(KEY_D_RESULT_SAME)

        diff_obj = DirNodeDiffObject(self.left_ftp_connect_obj, self.right_ftp_connect_obj, left_node, right_node)
        diff_obj.diff()
