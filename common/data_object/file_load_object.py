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

    def set_file_content(self, file_content):
        self.file_content = file_content


class SharedStorageFileLoadObject(FileLoadObject):
    def __init__(self, file_name, file_path, file_type, file_size, modification_time, root_key, environment_name):
        folder_path = COMPARE_FILE_PATH + root_key + "/" + environment_name
        create_folder(folder_path)

        self.local_path = folder_path + "/" + file_name
        self.environment_name = environment_name
        super().__init__(file_name, file_path, file_type, file_size, modification_time, self.local_path)

    def set_file_content(self, file_content):
        super().set_file_content(file_content)
