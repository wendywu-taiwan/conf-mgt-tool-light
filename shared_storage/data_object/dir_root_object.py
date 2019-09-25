from shared_storage.data_object.node_object import NodeObject
from shared_storage.properties.config import *
from RulesetComparer.properties.key import GIT_NAME
from common.data_object.ftp_connect_object import SharedStorageConnectionObject
from common.data_object.git_connect_object import SharedStorageGitConnectObject
from permission.models import FTPClient, Environment


class DirRootObject:
    def __init__(self, client_id, environment_id, folder, only_last_version):
        try:
            self.client_id = client_id
            self.environment = Environment.objects.get(id=environment_id)
            self.folder = folder
            self.only_last_version = only_last_version
            self.filter_modules = FILTER_MODULE_FOLDER_MAP.get(self.folder)
            self.node_object = NodeObject(folder, self.environment, None, 0, None)

            self.client = None
            self.dir_connect_obj = None
            self.parse_dir_connect_object()
        except Exception as e:
            raise e

    def parse_dir_connect_object(self):
        if self.environment.name == GIT_NAME:
            self.dir_connect_obj = SharedStorageGitConnectObject(self.only_last_version)
        else:
            self.client = FTPClient.objects.get(id=self.client_id)
            self.dir_connect_obj = SharedStorageConnectionObject(self.client.id, self.environment.id,
                                                                 self.folder, self.only_last_version)

    def update_compare_key(self, compare_key):
        self.dir_connect_obj.set_compare_key(compare_key)

    def generate_json(self):
        json = self.node_object.parse_node_json()
        return json
