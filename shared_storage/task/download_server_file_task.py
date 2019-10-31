from RulesetComparer.utils.fileManager import *
from shared_storage.properties.config import get_zip_file_folder_path, get_zip_file_full_path


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
        # self.copy_ruleset()
        self.archive_file()
        self.remove_copied_files()

    # def copy_ruleset(self):
    #     create_folder(self.copied_path)
    #     for rule_set_name in self.name_xml_list:
    #         resource_full_path = self.resource_path + "/" + rule_set_name
    #         copied_full_path = self.copied_path + "/" + rule_set_name
    #         info_log(self.LOG_CLASS, "copy file : %s" % rule_set_name)
    #         copyfile(resource_full_path, copied_full_path)

    def archive_file(self):
        download_file_name = timeUtil.get_format_current_time(TIME_FORMAT.get("year_month_date")) + "files"
        archive_file_with_arcname(self.resource_path, self.zip_file_folder_path, self.zip_file_full_path,
                                  download_file_name)

    def remove_copied_files(self):
        pass
        # copied_path_key = self.copied_path.split("/")[-3]
        # removed_path = get_rule_set_path("", "", copied_path_key)
        # info_log(self.LOG_CLASS, "removed folder = %s" % removed_path)
        # clear_folder(removed_path)
