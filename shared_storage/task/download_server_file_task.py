from RulesetComparer.utils.fileManager import *
from shared_storage.properties.config import get_zip_file_folder_path, get_zip_file_full_path, COMPARE_FILE_PATH


class DownloadServerFileTask:
    LOG_CLASS = "DownloadServerFileTask"

    def __init__(self, file_object_list):
        try:
            self.file_object_list = file_object_list
            self.resource_path = self.file_object_list[0].folder_path
            self.compare_hash_key = hash(self)
            self.zip_file_folder_path = get_zip_file_folder_path()
            self.zip_file_full_path = get_zip_file_full_path(self.compare_hash_key)
            self.execute()
        except Exception as e:
            raise e

    def execute(self):
        self.archive_file()
        self.remove_files()

    def archive_file(self):
        archive_file_with_arcname(self.resource_path, self.zip_file_folder_path, self.zip_file_full_path)

    def remove_files(self):
        download_folder_hash_key = self.resource_path.split("/")[-2]
        download_folder_path = COMPARE_FILE_PATH + download_folder_hash_key
        clear_folder(download_folder_path)
