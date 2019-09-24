from shared_storage.data_object.node_object import NodeObject
from shared_storage.properties.config import *
from common.utils.ftp_manager import SharedStorageConnectionObject
from permission.models import FTPClient, Environment


class DirRootObject:
    def __init__(self, client_id, environment_id, folder, only_last_version):
        try:
            self.client = FTPClient.objects.get(id=client_id)
            self.environment = Environment.objects.get(id=environment_id)
            self.folder = folder
            self.only_last_version = only_last_version
            self.ftp_connect_obj = SharedStorageConnectionObject(self.client.id, self.environment.id, folder,
                                                                 only_last_version)
            self.filter_modules = FILTER_MODULE_FOLDER_MAP.get(self.folder)
            self.node_object = NodeObject(folder, self.environment, None, 0, None)
            self.json_object = None

        except Exception as e:
            raise e

    def update_compare_key(self, compare_key):
        self.ftp_connect_obj.set_compare_key(compare_key)

    def generate_json(self):
        json = self.node_object.parse_node_json()
        return json
