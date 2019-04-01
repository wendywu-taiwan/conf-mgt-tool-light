import traceback
from lxml import etree
from RulesetComparer.utils.logger import *
from RulesetComparer.models import Environment, Country
from RulesetComparer.utils.fileManager import load_file
from RulesetComparer.properties.config import get_rule_set_path, get_rule_set_git_path, get_rule_set_full_file_name
from RulesetComparer.properties import config
from RulesetComparer.dataModel.xml.ruleSetObject import RulesetObject


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
    file_path = get_rule_set_path(env_name,
                                  country_name,
                                  compare_key)
    file_name_with_path = get_rule_set_full_file_name(file_path, rule_set_name)
    rule_set_file = load_file(file_name_with_path)
    return rule_set_file


def load_git_ruleset_with_name(country_name, rule_set_name):
    file_path = get_rule_set_git_path(country_name)
    file_name_with_path = get_rule_set_full_file_name(file_path, rule_set_name)
    rule_set_file = load_file(file_name_with_path)
    return rule_set_file


def build_ruleset_xml(rule_model_list):
    ruleset_file_xml = etree.Element('BRERuleListType')
    for rule in rule_model_list:
        ruleset_file_xml.append(rule.to_xml())

    xml_string = xml_to_string(ruleset_file_xml)
    print("build_ruleset_xml:" + xml_string)

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
