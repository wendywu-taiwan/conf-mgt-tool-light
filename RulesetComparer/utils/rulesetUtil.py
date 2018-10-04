from RulesetComparer.models import Environment,Country
from RulesetComparer.utils import fileManager
from django.conf import settings
from RulesetComparer.properties import dataKey as key


def load_local_rule_file_with_id(env_id, country_id, compare_key, rule_set_name):
    env = Environment.objects.get(id=env_id)
    country = Country.objects.get(id=country_id)

    if env.name == key.ENVIRONMENT_KEY_GIT:
        return load_local_git_file_with_name(country.name, rule_set_name)
    else:
        return load_local_rule_file_with_name(env.name, country.name, compare_key, rule_set_name)


def load_local_rule_file_with_name(env_name, country_name, compare_key, rule_set_name):
    # save file to specific path
    file_path = settings.RULESET_SAVED_PATH % (env_name,
                                               country_name,
                                               compare_key)

    file_name_with_path = settings.RULESET_SAVED_NAME % (file_path,
                                                         rule_set_name)
    rule_set_file = fileManager.load_file(file_name_with_path)
    return rule_set_file


def load_local_git_file_with_name(country_name, rule_set_name):
    file_path = settings.GIT_RULESET_SAVED_PATH % (settings.INT1_RULE_SET_LOCAL_REPOSITORY_NAME,
                                                   country_name)

    file_name_with_path = settings.RULESET_SAVED_NAME % (file_path,
                                                         rule_set_name)
    rule_set_file = fileManager.load_file(file_name_with_path)
    return rule_set_file
