import os
from common.data_object.dir_connect_object import DirConnectObject
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.utils.logger import *
from permission.models import Environment
from shared_storage.properties.config import *


class SharedStorageGitConnectObject(DirConnectObject):
    LOG_CLASS = "SharedStorageGitConnectObject"

    def __init__(self, only_last_version, branch=None):
        try:
            super().__init__()
            self.git_path = GIT_SHARE_STORAGE_ROOT
            self.root_path = DIR_GIT_SHARE_STORAGE_ROOT
            self.branch = self.parse_branch(branch)
            self.environment = Environment.objects.get(name=GIT_NAME)
            self.only_last_version = only_last_version
            self.git_manager = GitManager(self.git_path, self.branch)
            self.connect()
        except Exception as e:
            raise e

    @staticmethod
    def parse_branch(branch):
        if branch is None:
            branch = settings.GIT_BRANCH_DEVELOP
        return branch

    def connect(self):
        self.git_manager.pull()

    def disconnect(self):
        self.git_manager = None

    def set_root_hash_key(self, root_hash_key):
        super().set_root_hash_key(root_hash_key)

    def get_path_list_dir(self, path):
        path = self.root_path + path
        entry_list = list()
        dir_list = sorted(os.listdir(path))
        for file in dir_list:
            file_path = path + "/" + file

            entry = os.stat(file_path)
            entry_object = GitDirEntryObject(entry, file)
            entry_list.append(entry_object)
        return entry_list

    def get_latest_version(self, node_path):
        tmp_file = 'lastversion.dat'
        last_version_path = self.root_path + node_path + "/" + tmp_file
        last_version = self.get_path_file(last_version_path, COMPARE_FILE_PATH + tmp_file)
        return last_version

    def get_path_file(self, file_path, save_path):
        try:
            f = open(file_path, 'r')
            file_content = f.read()
        except UnicodeDecodeError:
            f = open(file_path, 'rb')
            file_content = f.read()
        return file_content.strip()

    def get_file_contents(self, file_load_object):
        file_path = self.root_path + file_load_object.file_path
        file_load_object.file_content = self.get_path_file(file_path, None)
        return file_load_object


class GitDirEntryObject:
    def __init__(self, entry, filename):
        self.entry = entry
        self.st_mode = entry.st_mode
        self.st_size = entry.st_size
        self.st_mtime = entry.st_mtime
        self.filename = filename
