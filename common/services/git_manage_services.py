from common.data_object.json_parser.git_country_path_edit import GitCountryPathEditParser, KEY_M_RULESET
from common.models import GitCountryPath


def update_git_country_path(json):
    data_list = GitCountryPathEditParser(json).data_list
    for data in data_list:
        git_country_path_obj, created = GitCountryPath.objects.get_or_create(id=data.id)
        git_country_path_obj.repo_path = data.repo_path
        git_country_path_obj.folder = data.folder
        git_country_path_obj.save()
    return json


def get_ruleset_git_path(country_name):
    git_country_path = GitCountryPath.objects.get(country__name=country_name, module__name=KEY_M_RULESET)
    return git_country_path.repo_path


def get_ruleset_git_country_path(country_name):
    git_country_path = GitCountryPath.objects.get(country__name=country_name, module__name=KEY_M_RULESET)
    return git_country_path.repo_path + "/" + git_country_path.folder
