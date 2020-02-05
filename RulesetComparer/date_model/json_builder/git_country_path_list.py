from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleRulesetBuilder
from RulesetComparer.properties.key import KEY_MODULE_DATA, KEY_GIT_COUNTRY_PATH_LIST, KEY_ID, \
    KEY_COUNTRY, KEY_REPO_PATH, KEY_FOLDER
from common.data_object.json_builder.country import CountryBuilder
from common.data_object.json_builder.module import ModuleBuilder
from permission.models import Module, Country


class GitCountryPathListBuilder(AdminConsoleRulesetBuilder):
    def __init__(self, user, git_country_paths):
        self.git_country_paths = git_country_paths
        AdminConsoleRulesetBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[KEY_GIT_COUNTRY_PATH_LIST] = self.generate_git_country_path_data()

    def generate_git_country_path_data(self):
        data_list = []
        for git_country_path in self.git_country_paths:
            module = Module.objects.get(id=git_country_path.get("module_id"))
            country = Country.objects.get(id=git_country_path.get("country_id"))
            data_object = {
                KEY_ID: git_country_path.get("id"),
                KEY_MODULE_DATA: ModuleBuilder(module).get_data(),
                KEY_COUNTRY: CountryBuilder(country).get_data(),
                KEY_REPO_PATH: git_country_path.get("repo_path"),
                KEY_FOLDER: git_country_path.get("folder")
            }
            data_list.append(data_object)
        return data_list
