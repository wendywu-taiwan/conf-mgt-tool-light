from permission.utils.permission_manager import *


class GitCountryPathEditParser:

    def __init__(self, json_data):
        self.git_country_path_list = json_data
        self.data_list = self.parse_git_country_paths()

    def parse_git_country_paths(self):
        data_list = list()
        for git_country_path in self.git_country_path_list:
            data_obj = GitCountryPathParser(git_country_path)
            data_list.append(data_obj)
        return data_list


class GitCountryPathParser:
    def __init__(self, git_country_path):
        self.id = git_country_path.get(KEY_ID)
        self.repo_path = git_country_path.get("repo_path")
        self.folder = git_country_path.get("folder")
