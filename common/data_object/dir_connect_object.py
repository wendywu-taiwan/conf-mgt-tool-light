from abc import abstractmethod


class DirConnectObject:
    LOG_CLASS = "DirConnectObject"

    def __init__(self):
        self.compare_key = None

    def set_compare_key(self, compare_key):
        self.compare_key = compare_key

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_path_list_dir(self, path):
        pass

    @abstractmethod
    def get_path_file(self, file_path, save_path):
        pass

    @abstractmethod
    def get_file_contents(self, file_load_object):
        pass
