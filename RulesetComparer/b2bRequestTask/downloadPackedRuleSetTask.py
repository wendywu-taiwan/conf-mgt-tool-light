import traceback
import zipfile
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.utils.fileManager import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.properties.config import *
from RulesetComparer.b2bRequestTask.downloadRuleSetTask import DownloadRuleSetTask
from shutil import copyfile


class DownloadPackedRuleSetTask:
    LOG_CLASS = "DownloadPackedRuleSetTask"

    def __init__(self, env_id, country_id, rule_set_name_list):
        try:
            self.compare_hash_key = hash(self)
            self.environment = Environment.objects.get(id=env_id)
            self.country = Country.objects.get(id=country_id)
            self.name_list = rule_set_name_list
            self.rule_set_folder_path = get_rule_set_path(self.compare_hash_key,
                                                          self.environment.name,
                                                          self.country.name)
            self.zip_file_path = get_rule_set_zip_file_name(self.compare_hash_key)
            self.execute()
        except Exception:
            traceback.print_exc()
            error_log(traceback.format_exc())

    def execute(self):
        if self.environment.name == GIT.get("environment_name"):
            self.get_file_from_git()
        else:
            self.get_file_from_server()
        self.remove_rule_files()

    def get_file_from_git(self):
        # update git to latest code
        git_path = get_rule_set_git_path("")
        git_country_path = get_rule_set_git_path(self.country.name)
        manager = GitManager(git_path, settings.GIT_BRANCH_DEVELOP)
        manager.pull()

        # copy file from git folder to ruleset folder
        create_folder(self.rule_set_folder_path)
        for rule_set_name in self.name_list:
            resource_path = git_country_path + "/" + rule_set_name
            dst_path = self.rule_set_folder_path + "/" + rule_set_name
            print("resource_path =" + resource_path)
            print("dst_path =" + dst_path)
            copyfile(resource_path, dst_path)

        # zip file
        self.archive_folder()

    def get_file_from_server(self):
        # download ruleset
        for name in self.name_list:
            task = DownloadRuleSetTask(self.environment.id, self.country.id, name, self.compare_hash_key)
            # should handle download result

        # zip file
        self.archive_folder()

    def archive_folder(self):
        print("zip_file_dst = " + self.zip_file_path)
        zip_handler = zipfile.ZipFile(self.zip_file_path, mode='w', compression=zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(self.rule_set_folder_path):
            for file in files:
                zip_handler.write(os.path.join(root, file))
        zip_handler.close()

    def remove_rule_files(self):
        file_path = get_rule_set_path("", "", self.compare_hash_key)
        clear_folder(file_path)

