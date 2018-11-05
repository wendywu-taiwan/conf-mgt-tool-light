from RulesetComparer.models import Environment, Country
from RulesetComparer.utils.fileManager import load_file
from RulesetComparer.properties.config import get_rule_set_full_file_name
from RulesetComparer.properties import dataKey as key
from RulesetComparer.properties.config import get_rule_set_path, get_rule_set_git_path


def load_rule_file_with_id(env_id, country_id, compare_key, rule_set_name):
    env = Environment.objects.get(id=env_id)
    country = Country.objects.get(id=country_id)

    if env.name == key.ENVIRONMENT_KEY_GIT:
        return load_git_file_with_name(country.name, rule_set_name)
    else:
        return load_rule_file_with_name(env.name, country.name, compare_key, rule_set_name)


def load_rule_file_with_name(env_name, country_name, compare_key, rule_set_name):
    file_path = get_rule_set_path(env_name,
                                  country_name,
                                  compare_key)
    file_name_with_path = get_rule_set_full_file_name(file_path, rule_set_name)
    rule_set_file = load_file(file_name_with_path)
    return rule_set_file


def load_git_file_with_name(country_name, rule_set_name):
    file_path = get_rule_set_git_path(country_name)
    file_name_with_path = get_rule_set_full_file_name(file_path, rule_set_name)
    rule_set_file = load_file(file_name_with_path)
    return rule_set_file
