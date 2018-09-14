from RulesetComparer.services import RuleSetService
from django.shortcuts import render


def page_compare_select(request):
    return render(request, "ruleset_compare_select.html")


def page_compare_rule_list(request):
    country = request.POST.get('env1')
    environment1 = request.POST.get('env2')
    environment2 = request.POST.get('country')
    response_model = RuleSetService.compare_rule_list(RuleSetService(),
                                                      environment1,
                                                      environment2,
                                                      country)
    return render(request, "ruleset_compare_file_list_result.html", response_model.get_response_json())


def page_compare_rule_detail(request):
    country = request.POST.get('detail_country')
    environment = request.POST.get('detail_env')
    rule_set_name = request.POST.get('detail_rule_name')

    response_model = RuleSetService.get_rule_from_b2b(environment, country, rule_set_name)
    return render(request, "ruleset_show_detail.html", response_model.get_response_json())


def page_compare_rule_diff(request):
    country = request.POST.get('diff_country')
    environment1 = request.POST.get('diff_env1')
    environment2 = request.POST.get('diff_env2')
    rule_set_name = request.POST.get('diff_rule_name')
    response_model = RuleSetService.compare_rule_set(environment1,
                                                     environment2,
                                                     country,
                                                     rule_set_name)
    return render(request, "ruleset_show_diff.html", response_model.get_response_json())


def get_rule_list(request, environment, country):
    response_model = RuleSetService.get_rule_list_from_b2b(environment, country)
    return response_model.get_response_json()


def get_rule_set(request, environment, country, rule_set_name):
    response_model = RuleSetService.get_rule_from_b2b(environment, country, rule_set_name)
    return render(request, "ruleset_show_detail.html", response_model.get_response_json())


def compare_rule_list(request, country, environment1, environment2):
    response_model = RuleSetService.compare_rule_list(RuleSetService(),
                                                      environment1,
                                                      environment2,
                                                      country)

    return render(request, "ruleset_compare_file_list_result.html", response_model.get_response_json())


def compare_rule_set(request, country, environment1, environment2, rule_set_name):
    response_model = RuleSetService.compare_rule_set(environment1,
                                                     environment2,
                                                     country,
                                                     rule_set_name)
    return render(request, "ruleset_show_diff.html", response_model.get_response_json())
