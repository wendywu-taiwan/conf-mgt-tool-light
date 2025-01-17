from shared_storage.properties.config import COMPARE_FILE_PATH
from RulesetComparer.utils.fileManager import create_folder


class FileLoadObject:
    def __init__(self, file_name, file_path, file_type, file_size, modification_time, local_path):
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type
        self.file_size = file_size
        self.local_path = local_path
        self.modification_time = modification_time
        self.file_content = None
        self.file_content_bytes = None

    def set_file_content(self, file_content):
        if isinstance(file_content, bytes):
            self.file_content = file_content.decode('utf-8', errors='ignore')
            self.file_content_bytes = file_content
        else:
            self.file_content = file_content
            self.file_content_bytes = file_content.encode('utf-8', errors='ignore')


class SharedStorageFileLoadObject(FileLoadObject):
    def __init__(self, file_name, file_path, file_type, file_size, modification_time, root_key, environment_name):
        self.folder_path = COMPARE_FILE_PATH + root_key + "/" + environment_name
        create_folder(self.folder_path)

        self.local_path = self.folder_path + "/" + file_name
        self.environment_name = environment_name
        super().__init__(file_name, file_path, file_type, file_size, modification_time, self.local_path)

    def set_file_content(self, file_content):
        super().set_file_content(file_content)
