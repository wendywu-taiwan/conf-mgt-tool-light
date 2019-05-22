import traceback
from RulesetComparer.utils.fileManager import *
from RulesetComparer.properties.config import *
from shutil import copyfile


class PackedRulesetsTask:
    LOG_CLASS = "PackedRulesetsTask"

    def __init__(self, rule_name_xml_list, resource_path, copied_path):
        try:
            self.compare_hash_key = hash(self)
            self.name_xml_list = rule_name_xml_list
            self.resource_path = resource_path
            self.copied_path = copied_path
            self.zip_file = get_rule_set_zip_file_name(self.compare_hash_key)

            info_log(self.LOG_CLASS, "resource_path = %s" % resource_path)
            info_log(self.LOG_CLASS, "copied_path = %s" % copied_path)
            self.execute()
        except Exception as e:
            raise e

    def execute(self):
        self.copy_ruleset()
        self.archive_file()
        self.remove_copied_files()

    def copy_ruleset(self):
        create_folder(self.copied_path)
        for rule_set_name in self.name_xml_list:
            resource_full_path = self.resource_path + "/" + rule_set_name
            copied_full_path = self.copied_path + "/" + rule_set_name
            info_log(self.LOG_CLASS, "copy file : %s" % rule_set_name)
            copyfile(resource_full_path, copied_full_path)

    def archive_file(self):
        # RulesetComparer/rulesets/zip
        zip_file_path = get_full_file_path("rule_set_zip_file_path")
        zip_file_full_path = self.zip_file

        # to have single folder ruleset in zip file
        arcname_prefix = "ruleset/"
        archive_file_with_arcname(self.copied_path, zip_file_path, zip_file_full_path, arcname_prefix)

    def remove_copied_files(self):
        copied_path_key = self.copied_path.split("/")[-3]
        removed_path = get_rule_set_path("", "", copied_path_key)
        info_log(self.LOG_CLASS, "removed folder = %s" % removed_path)
        clear_folder(removed_path)
