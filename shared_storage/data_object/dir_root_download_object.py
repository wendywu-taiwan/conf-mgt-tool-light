from abc import abstractmethod

from shared_storage.data_object.dir_root_object import DirRootObject
from shared_storage.data_object.node_object import NodeObject


class DirRootDownloadObject(DirRootObject):
    def __init__(self, region_id, environment_id, folder_paths):
        DirRootObject.__init__(self, region_id, environment_id, folder_paths[0], False)
        self.folder_paths = folder_paths
        self.root_hash_key = str(hash(self))
        self.update_root_hash_key(self.root_hash_key)

    def download_node_files(self):
        file_object_list = list()
        for folder_path in self.folder_paths:
            file_name = folder_path.split("/")[-1]
            node_object = NodeObject(file_name, self.environment, None, 0, None)
            node_object.path = folder_path
            file_object = self.download_node_file(node_object)
            file_object_list.append(file_object)
        return file_object_list

    @abstractmethod
    def download_node_file(self, node_object):
        pass


class DirRootServerDownloadObject(DirRootDownloadObject):
    def __init__(self, region_id, environment_id, folder_paths):
        DirRootDownloadObject.__init__(self, region_id, environment_id, folder_paths)

    def download_node_files(self):
        return super().download_node_files()

    def download_node_file(self, node_object):
        file_object = node_object.download_files(self.root_hash_key, self.dir_connect_obj)
        return file_object


class DirRootGitDownloadObject(DirRootDownloadObject):
    def __init__(self, region_id, environment_id, folder_paths):
        DirRootDownloadObject.__init__(self, region_id, environment_id, folder_paths)

    def download_node_files(self):
        return super().download_node_files()

    def download_node_file(self, node_object):
        file_object = node_object.download_git_files(self.root_hash_key, self.dir_connect_obj)
        return file_object


class DirRootExistDownloadObject(DirRootDownloadObject):
    def __init__(self, region_id, environment_id, folder_paths, resource_hash_key):
        self.resource_hash_key = resource_hash_key
        DirRootDownloadObject.__init__(self, region_id, environment_id, folder_paths)

    def download_node_files(self):
        return super().download_node_files()

    def download_node_file(self, node_object):
        file_object = node_object.download_exist_files(self.resource_hash_key, self.root_hash_key)
        return file_object
