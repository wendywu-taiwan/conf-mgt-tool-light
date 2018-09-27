from django.shortcuts import render

from RulesetComparer.models import B2BRuleSetServer, Country, Environment
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, RuleListItemSerializer, \
    RuleSerializer
from RulesetComparer.services.services import RuleSetService

REQUEST_GET = 'GET'
REQUEST_POST = 'POST'


def environment_select(request):
    country_ids = B2BRuleSetServer.objects.get_accessible_country_ids()
    environments_ids = B2BRuleSetServer.objects.get_accessible_environment_ids()
    country_list = Country.objects.country_list(country_ids)
    environment_list = Environment.objects.environment_list(environments_ids)

    response = {"countries": CountrySerializer(country_list, many=True).data,
                "environments": EnvironmentSerializer(environment_list, many=True).data}

    if request.method == REQUEST_GET:
        return render(request, "environment_select.html", response)

    elif request.method == REQUEST_POST:
        country_id = request.POST.get('country')
        base_env_id = request.POST.get('base_env')
        compare_env_id = request.POST.get('compare_env')

        if not country_id or not base_env_id or not compare_env_id or base_env_id == compare_env_id:
            return render(request, "environment_select.html", response)
        else:
            data = compare_rule_list_item_data(country_id, base_env_id, compare_env_id)
            return render(request, "rule_item_list.html", data)


def rule_detail(request, env_id, country_id, compare_key, rule_name):
    rules_model = RuleSetService.get_detail_rule_data(env_id, country_id, compare_key, rule_name)
    rules_data = RuleSerializer(rules_model.get_rules_data_array(), many=True).data
    data = {"rule_name": rule_name,
            "rule_data": rules_data}
    return render(request, "rule_show_detail.html", data)


def rule_diff(request, base_env_id, compare_env_id, country_id, compare_key, rule_name):
    response_model = RuleSetService.diff_rule_set(base_env_id,
                                                  compare_env_id,
                                                  country_id,
                                                  compare_key,
                                                  rule_name)
    return render(request, "rule_show_diff.html", response_model.get_response_json())


def compare_rule_list_item_data(country_id, base_env_id, compare_env_id):
    task = RuleSetService.compare_rule_list_rule_set(base_env_id,
                                                     compare_env_id,
                                                     country_id)

    base_env_data = EnvironmentSerializer(Environment.objects.get(id=base_env_id)).data
    compare_env_data = EnvironmentSerializer(Environment.objects.get(id=compare_env_id)).data
    country_data = CountrySerializer(Country.objects.get(id=country_id)).data
    add_list = RuleListItemSerializer(task.get_add_rule_list(), many=True).data
    minus_list = RuleListItemSerializer(task.get_minus_rule_list(), many=True).data
    normal_list = RuleListItemSerializer(task.get_normal_rule_list(), many=True).data
    modify_list = RuleListItemSerializer(task.get_modify_rule_list(), many=True).data

    data = {"country": country_data,
            "base_env": base_env_data,
            "compare_env": compare_env_data,
            "compare_hash_key": task.compare_hash_key,
            "add_list": add_list,
            "minus_list": minus_list,
            "normal_list": normal_list,
            "modify_list": modify_list}
    return data


# todo : return json rule list response
def json_rule_list(request, environment, country):
    response_model = RuleSetService.get_rule_list_from_b2b(environment, country)
    return response_model.get_response_json()


# todo : return json rule detail
def json_rule_detail(request, country, env, rule_set_name):
    response_model = RuleSetService.get_rule_from_b2b(env, country, rule_set_name)
    return render(request, "rule_show_detail.html", response_model.get_response_json())

# todo : return json rule diff result
def json_rule_diff(request, base_env_id, compare_env_id, country_id, compare_key):
    country = request.POST.get('diff_country')
    environment1 = request.POST.get('diff_env1')
    environment2 = request.POST.get('diff_env2')
    rule_set_name = request.POST.get('diff_rule_name')
    response_model = RuleSetService.compare_rule_set(environment1,
                                                     environment2,
                                                     country,
                                                     rule_set_name)
    return render(request, "rule_show_diff.html", response_model.get_response_json())
