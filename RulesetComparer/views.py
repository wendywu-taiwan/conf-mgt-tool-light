from RulesetComparer.services import RuleSetService
from django.shortcuts import render


def page_header(request):
    return render(request, "bootstrap_header.html")


def page_compare_select(request):
    return render(request, "ruleset_compare_select.html")


def get_rule_list(request, environment, country):
    response_model = RuleSetService.get_rule_list_from_b2b(environment, country)
    return response_model.get_response_json()


def get_rule_set(request, environment, country, rule_set_name):
    response_model = RuleSetService.get_rule_from_b2b(environment, country, rule_set_name)
    return response_model.get_response_json()


def download_rule_set_test(request):
    response_model = RuleSetService.download_rule_set_from_b2b(RuleSetService(),
                                                               'Local',
                                                               'TW')
    return render(request, "temp_query_compare_ruleset.html", response_model.get_response_json())


def download_single_rule_set(request, environment, country, rule_set_name):
    response_model = RuleSetService.download_single_rule_set_from_b2b(environment,
                                                                      country,
                                                                      rule_set_name)
    return response_model.get_response_json()
    # response_model = RuleSetService.download_single_rule_set(environment, country, rule_set_name)
    # return response_model.get_response_json()


def download_rule_set_from_git(request, country):
    return RuleSetService.download_rule_set_from_git(country)


def compare_country_rule_set(request, country):
    response_model = RuleSetService.compare_rule_set(country)
    return response_model.get_response_json()
