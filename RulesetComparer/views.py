from RulesetComparer.services.services import RuleSetService
from django.shortcuts import render
from RulesetComparer.models import B2BRuleSetServer, Country, Environment
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, RuleListItemSerializer

REQUEST_GET = 'GET'
REQUEST_POST = 'POST'


def page_compare_select(request):
    country_ids = B2BRuleSetServer.objects.filter(accessible=True).values('country_id').distinct()
    environments_ids = B2BRuleSetServer.objects.filter(accessible=True).values('environment_id').distinct()
    country_list = Country.objects.country_list(country_ids)
    environment_list = Environment.objects.environment_list(environments_ids)

    country_serializer = CountrySerializer(country_list, many=True)
    env_serializer = EnvironmentSerializer(environment_list, many=True)

    response = {"countries": country_serializer.data,
                "environments": env_serializer.data}

    if request.method == REQUEST_GET:
        return render(request, "ruleset_compare_select.html", response)

    elif request.method == REQUEST_POST:
        country = request.POST['env1']
        environment1 = request.POST['env2']
        environment2 = request.POST['country']

        if not country or not environment1 or not environment2 or environment1 == environment2:
            return render(request, "ruleset_compare_select.html", response)
        else:
            return page_compare_rule_list_item(request)


def page_compare_rule_list_item(request):
    country = request.POST['env1']
    environment1 = request.POST['env2']
    environment2 = request.POST['country']
    task = RuleSetService.compare_rule_list_rule_set(environment1,
                                                     environment2,
                                                     country)

    add_list = RuleListItemSerializer(task.get_add_rule_list(), many=True).data
    minus_list = RuleListItemSerializer(task.get_minus_rule_list(), many=True).data
    normal_list = RuleListItemSerializer(task.get_normal_rule_list(), many=True).data
    modify_list = RuleListItemSerializer(task.get_modify_rule_list(), many=True).data
    data = {"add_list": add_list, "minus_list": minus_list, "normal_list": normal_list, "modify_list": modify_list}
    return render(request, "ruleset_compare_item_list.html", data)


def page_compare_rule_list(request):
    country = request.POST['env1']
    environment1 = request.POST['env2']
    environment2 = request.POST['country']
    task = RuleSetService.compare_rule_list_rule_set(environment1,
                                                     environment2,
                                                     country)

    add_list = RuleListItemSerializer(task.get_add_rule_list(), many=True)
    minus_list = RuleListItemSerializer(task.get_minus_rule_list(), many=True)
    normal_list = RuleListItemSerializer(task.get_normal_rule_list(), many=True)
    modify_list = RuleListItemSerializer(task.get_modify_rule_list(), many=True)
    data = {"add_list": add_list, "minus_list": minus_list, "normal_list": normal_list, "modify_list": modify_list}
    return render(request, "ruleset_compare_file_list_result.html", data)


def page_compare_rule_detail(request):
    country = request.POST.get('detail_country')
    environment = request.POST.get('detail_env')
    rule_set_name = request.POST.get('detail_rule_name')

    response_model = RuleSetService.get_rule_from_b2b(environment, country, rule_set_name)
    return render(request, "ruleset_show_detail.html", response_model.get_response_json())


def compare_rule_detail(request, country, env, rule_set_name):
    response_model = RuleSetService.get_rule_from_b2b(env, country, rule_set_name)
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
