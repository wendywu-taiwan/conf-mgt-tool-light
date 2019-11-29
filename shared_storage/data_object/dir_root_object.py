from shared_storage.data_object.node_object import NodeObject
from shared_storage.properties.config import *
from RulesetComparer.properties.key import GIT_NAME, KEY_D_RESULT_SAME
from common.data_object.ftp_connect_object import SharedStorageConnectionObject
from common.data_object.git_connect_object import SharedStorageGitConnectObject
from permission.models import FTPClient, Environment


class DirRootObject:
    def __init__(self, region_id, environment_id, folder, only_last_version):
        self.region_id = region_id
        self.environment = Environment.objects.get(id=environment_id)
        self.folder = folder
        self.only_last_version = only_last_version
        self.filter_modules = FILTER_MODULE_FOLDER_MAP.get(self.folder)
        self.node_object = NodeObject(folder, self.environment, None, 0, None)
        self.node_object.set_diff_result(KEY_D_RESULT_SAME)
        self.client = None
        self.dir_connect_obj = None
        self.parse_dir_connect_object()

    def parse_dir_connect_object(self):
        if self.environment.name == GIT_NAME:
            self.dir_connect_obj = SharedStorageGitConnectObject(self.only_last_version, self.folder)
        else:
            self.dir_connect_obj = SharedStorageConnectionObject(self.region_id, self.environment.id,
                                                                 self.only_last_version, self.folder)

    def update_root_hash_key(self, root_hash_key):
        self.dir_connect_obj.set_root_hash_key(root_hash_key)

    def generate_compare_result_json(self):
        json = self.node_object.parse_root_node_json()
        return json

    def generate_compare_result_mail_json(self, self_only_list, self_no_list, different_list):
        self.node_object.parse_mail_node_json(self_only_list, self_no_list, different_list)

    def generate_files_list_json(self):
        return self.node_object.parse_files_list_json()

    def generate_filtered_files_list_json(self, result_list, filter_keys):
        self.node_object.parse_filtered_files_list_json(self.dir_connect_obj, result_list, filter_keys)
