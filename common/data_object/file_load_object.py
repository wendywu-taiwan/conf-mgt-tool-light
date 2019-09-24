from shared_storage.properties.config import COMPARE_FILE_PATH


class FileLoadObject:
    def __init__(self, file_name, file_path, file_type, file_size, local_path):
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type
        self.file_size = file_size
        self.local_path = local_path
        self.file_content = None

    def set_file_content(self, file_content):
        self.file_content = file_content


class SharedStorageFileLoadObject(FileLoadObject):
    def __init__(self, file_name, file_path, file_type, file_size):
        self.local_path = COMPARE_FILE_PATH + file_name
        super().__init__(file_name, file_path, file_type, file_size, self.local_path)

    def set_file_content(self, file_content):
        super().set_file_content(file_content)
