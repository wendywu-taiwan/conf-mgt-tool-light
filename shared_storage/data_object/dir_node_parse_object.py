from abc import abstractmethod

from RulesetComparer.utils.logger import info_log
from RulesetComparer.properties.key import *
from RulesetComparer.utils.stringFilter import string_filter
from shared_storage.data_object.node_object import NodeObject
from shared_storage.properties.config import LATEST_VERSION_PARENT_FOLDER, LATEST_VERSION_GRAND_PARENT_FOLDER


class DirNodeParseBaseObject:
    LOG_CLASS = "DirNodeParseBaseObject"

    def __init__(self, connect_obj, node):
        self.connect_obj = connect_obj
        self.parent_node = node
        self.entry_list = connect_obj.get_path_list_dir(self.parent_node.path)
        self.root_key = self.connect_obj.root_hash_key

    def parse_nodes(self):
        index = 0
        for entry in self.entry_list:
            node = self.parse_node(entry, index)
            self.parse_child_nodes(node)

    def parse_node(self, entry, index):
        node = NodeObject(entry.filename, self.parent_node.environment, self.parent_node, index, entry.st_mode)
        node.set_size(entry.st_size)
        node.set_modification_time(entry.st_mtime)
        node.node_hash_key = hash(node)
        self.parent_node.add_child_node_list(node)

        info_log(self.LOG_CLASS,
                 "parse_node , index:" + str(node.index) + ", depth: " + str(node.depth) + ", path: " + node.path)
        return node

    @abstractmethod
    def parse_child_nodes(self, node):
        pass


class DirNodeParseLatestVersionParentObject(DirNodeParseBaseObject):
    LOG_CLASS = "DirNodeParseLatestVersionParentObject"

    def __init__(self, connect_obj, node):
        DirNodeParseBaseObject.__init__(self, connect_obj, node)

    def parse_nodes(self):
        super().parse_nodes()

    def parse_child_nodes(self, node):
        if string_filter(node.path, LATEST_VERSION_PARENT_FOLDER):
            latest_version = self.connect_obj.get_latest_version(node.path)
            info_log(self.LOG_CLASS, "latest_version:" + str(latest_version))
            child_node_parser = DirNodeParseFilteredObject(self.connect_obj, node, latest_version)
        elif string_filter(node.path, LATEST_VERSION_GRAND_PARENT_FOLDER):
            child_node_parser = DirNodeParseLatestVersionParentObject(self.connect_obj, node)
        else:
            child_node_parser = DirNodeParseObject(self.connect_obj, node)
        child_node_parser.parse_nodes()


class DirNodeParseFilteredLatestVersionParentObject(DirNodeParseLatestVersionParentObject):
    LOG_CLASS = "DirNodeParseFilteredLatestVersionParentObject"

    def __init__(self, connect_obj, node, filters):
        DirNodeParseLatestVersionParentObject.__init__(self, connect_obj, node)
        self.filters = filters

    def parse_nodes(self):
        index = 0
        for entry in self.entry_list:
            name = entry.filename

            if name not in self.filters:
                continue

            node = super().parse_node(entry, index)
            self.parse_child_nodes(node)

    def parse_child_nodes(self, node):
        super().parse_child_nodes(node)


class DirNodeParseFolderObject(DirNodeParseBaseObject):
    LOG_CLASS = "DirNodeParseFolderObject"

    def __init__(self, connect_obj, node):
        DirNodeParseBaseObject.__init__(self, connect_obj, node)

    def parse_nodes(self):
        super().parse_nodes()

    def parse_child_nodes(self, node):
        node_parser_obj = DirNodeParseFolderObject(self.connect_obj, node)
        node_parser_obj.parse_nodes()


class DirNodeParseObject(DirNodeParseBaseObject):
    LOG_CLASS = "DirNodeParseObject"

    def __init__(self, connect_obj, node):
        DirNodeParseBaseObject.__init__(self, connect_obj, node)

    def parse_nodes(self):
        super().parse_nodes()

    def parse_child_nodes(self, node):
        if node.type is KEY_FOLDER:
            node_parser_obj = DirNodeParseObject(self.connect_obj, node)
            node_parser_obj.parse_nodes()


class DirNodeParseFilteredObject(DirNodeParseObject):
    LOG_CLASS = "DirNodeParseFilteredObject"

    def __init__(self, connect_obj, node, filters):
        DirNodeParseObject.__init__(self, connect_obj, node)
        self.filters = filters

    def parse_nodes(self):
        index = 0
        for entry in self.entry_list:
            name = entry.filename

            if name not in self.filters:
                continue

            node = super().parse_node(entry, index)
            self.parse_child_nodes(node)

    def parse_child_nodes(self, node):
        super().parse_child_nodes(node)
