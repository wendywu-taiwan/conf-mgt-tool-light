from RulesetComparer.utils.fileManager import *
from shared_storage.properties.config import get_zip_file_folder_path, get_zip_file_full_path, COMPARE_FILE_PATH
from common.properties.time_format import ARCHIVE_FOLDER_FORMAT
from RulesetComparer.utils.timeUtil import get_format_current_time


class DownloadServerFileTask:
    LOG_CLASS = "DownloadServerFileTask"

    def __init__(self, file_object_list):
        self.file_object_list = file_object_list
        self.resource_path = self.file_object_list[0].folder_path
        self.compare_hash_key = hash(self)
        self.zip_file_folder_path = get_zip_file_folder_path()
        self.zip_file_full_path = get_zip_file_full_path(self.compare_hash_key)
        self.execute()

    def execute(self):
        self.archive_file()
        self.remove_files()

    def archive_file(self):
        # if arcname_prefix contains {folder_name}/ , after unzip will show folder/files
        create_folder(self.zip_file_folder_path)
        zip_handler = zipfile.ZipFile(self.zip_file_full_path, mode='w')
        current_time = get_format_current_time(ARCHIVE_FOLDER_FORMAT)

        for file_object in self.file_object_list:
            # resource file path
            absname = os.path.abspath(os.path.join(file_object.folder_path, file_object.file_name))
            # destination file structure ex. tw/audacx/0001/abc.properties
            arcname = current_time + file_object.file_path
            zip_handler.write(absname, arcname)

        zip_handler.close()

    def remove_files(self):
        download_folder_hash_key = self.resource_path.split("/")[-2]
        download_folder_path = COMPARE_FILE_PATH + download_folder_hash_key
        clear_folder(download_folder_path)
