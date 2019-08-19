import traceback
from lxml import etree
from shutil import copyfile
from RulesetComparer.utils.logger import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.utils.fileManager import load_file, create_folder
from RulesetComparer.properties.config import get_rule_set_path, get_rule_set_git_path, get_rule_set_full_file_name
from RulesetComparer.properties import config
from RulesetComparer.date_model.xml.ruleset import RulesetObject


def load_rule_file_with_path(path, ruleset_name):
    file_name_with_path = get_rule_set_full_file_name(path, ruleset_name)
    rule_set_file = load_file(file_name_with_path)
    return rule_set_file


def load_rule_file_with_id(env_id, country_id, compare_key, rule_set_name):
    env = Environment.objects.get(id=env_id)
    country = Country.objects.get(id=country_id)

    return load_ruleset_with_name(rule_set_name, env.name, country.name, compare_key)


def load_ruleset_with_name(rule_set_name, env_name, country_name, compare_key):
    if env_name == config.GIT.get("environment_name"):
        return load_git_ruleset_with_name(country_name, rule_set_name)
    else:
        return load_server_ruleset_with_name(env_name, country_name, compare_key, rule_set_name)


def load_server_ruleset_with_name(env_name, country_name, compare_key, rule_set_name):
    file_path = get_rule_set_path(env_name, country_name, compare_key)
    return load_rule_file_with_path(file_path, rule_set_name)


def load_git_ruleset_with_name(country_name, rule_set_name):
    file_path = get_rule_set_git_path(country_name)
    return load_rule_file_with_path(file_path, rule_set_name)


def load_backup_server_version_rs(backup_key, ruleset_name):
    rs_path = get_rs_path_backup_server_version(backup_key, ruleset_name)
    ruleset_xml = load_file(rs_path)
    return ruleset_xml


def load_backup_applied_version_rs(backup_key, ruleset_name):
    rs_path = get_rs_path_backup_applied_version(backup_key, ruleset_name)
    ruleset_xml = load_file(rs_path)
    return ruleset_xml


def load_backup_ruleset_with_name(env_name, country_name, selected_folder_name, ruleset_name):
    backup_folder_path = get_ruleset_backup_path(env_name, country_name, selected_folder_name)
    return load_rule_file_with_path(backup_folder_path, ruleset_name)


def build_ruleset_xml(rule_model_list):
    ruleset_file_xml = etree.Element('BRERuleListType')
    for rule in rule_model_list:
        ruleset_file_xml.append(rule.to_xml())

    xml_string = xml_to_string(ruleset_file_xml)

    return xml_string


def load_ruleset_object(rule_name, country_name, env_name, compare_hash_key):
    try:
        rule_set_file = load_ruleset_with_name(rule_name, env_name, country_name, compare_hash_key)
        rules_module = RulesetObject(rule_set_file, rule_name)
        return rules_module
    except Exception as e:
        error_log(traceback.format_exc())
        return None


def load_rule_module_from_file(ruleset_name, ruleset_file):
    try:
        ruleset_module = RulesetObject(ruleset_file, ruleset_name)
        return ruleset_module
    except Exception as e:
        error_log(traceback.format_exc())
        return None


def xml_to_string(xml):
    return etree.tostring(xml, encoding="unicode", pretty_print=True)


def copy_rulesets(ruleset_name_list, source_folder_path, target_folder_path):
    create_folder(target_folder_path)
    for ruleset_name in ruleset_name_list:
        source_file_path = source_folder_path + "/" + ruleset_name
        target_file_path = target_folder_path + "/" + ruleset_name
        copyfile(source_file_path, target_file_path)


def copy_ruleset(ruleset_name, source_folder_path, target_folder_path):
    create_folder(target_folder_path)
    source_file_path = source_folder_path + "/" + ruleset_name
    target_file_path = target_folder_path + "/" + ruleset_name
    copyfile(source_file_path, target_file_path)
