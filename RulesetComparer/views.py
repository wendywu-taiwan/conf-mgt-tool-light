from RulesetComparer.services import RuleSetService
from RulesetComparer.utils import rulesetComparer


def download_rule_set(request, environment, country):
    response_model = RuleSetService.download_rule_set(RuleSetService(), environment, country)
    return response_model.get_response_json()


def download_single_rule_set(request, environment, country, rule_set_name):
    rulesetComparer.get_rules_key_list()
    # response_model = RuleSetService.download_single_rule_set(environment, country, rule_set_name)
    # return response_model.get_response_json()


def download_rule_set_from_git(request, country):
    return RuleSetService.download_rule_set_from_git(country)


def compare_country_rule_set(request, country):
    return RuleSetService.compare_rule_set(country)
