from django.shortcuts import render
from RulesetComparer.models import B2BRuleSetServer, Country, Environment
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, RuleListItemSerializer, \
    RuleSerializer, ModifiedRuleValueSerializer
from RulesetComparer.services.services import RuleSetService
from RulesetComparer.properties import dataKey as key
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, RuleListItemSerializer
from RulesetComparer.utils.gitManager import GitManager
from django.conf import settings

REQUEST_GET = 'GET'
REQUEST_POST = 'POST'


def environment_select(request):
    country_ids = B2BRuleSetServer.objects.get_accessible_country_ids()
    environments_ids = B2BRuleSetServer.objects.get_accessible_environment_ids()
    country_list = Country.objects.country_list(country_ids)
    environment_list = Environment.objects.environment_list(environments_ids)

    response = {key.ENVIRONMENT_SELECT_COUNTRY: CountrySerializer(country_list, many=True).data,
                key.ENVIRONMENT_SELECT_ENVIRONMENT: EnvironmentSerializer(environment_list, many=True).data}

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
    data = {key.RULE_KEY_RULE_NAME: rule_name,
            key.RULE_KEY_RULE_DATA: rules_data}
    return render(request, "rule_show_detail.html", data)


def rule_diff(request, base_env_id, compare_env_id, country_id, compare_key, rule_name):
    compare_result = RuleSetService.diff_rule_set(base_env_id, compare_env_id, country_id,
                                                  compare_key, rule_name)
    base_env = Environment.objects.get(id=base_env_id)
    compare_env = Environment.objects.get(id=compare_env_id)
    add_list = RuleSerializer(compare_result[key.RULE_LIST_ITEM_TABLE_TYPE_ADD], many=True).data
    remove_list = RuleSerializer(compare_result[key.RULE_LIST_ITEM_TABLE_TYPE_REMOVE], many=True).data
    modify_list = ModifiedRuleValueSerializer(compare_result[key.RULE_LIST_ITEM_TABLE_TYPE_MODIFY], many=True).data
    normal_list = RuleSerializer(compare_result[key.RULE_LIST_ITEM_TABLE_TYPE_NORMAL], many=True).data

    data = {
        key.RULE_KEY_RULE_DATA: rule_name,
        key.RULE_DIFF_KEY_BASE_ENV_NAME: base_env.name,
        key.RULE_DIFF_KEY_COMPARED_ENV_NAME: compare_env.name,
        key.RULE_DIFF_KEY_ADD_LIST: add_list,
        key.RULE_DIFF_KEY_REMOVE_LIST: remove_list,
        key.RULE_DIFF_KEY_MODIFY_LIST: modify_list,
        key.RULE_DIFF_KEY_NORMAL_LIST: normal_list
    }
    return render(request, "rule_show_diff.html", data)


def compare_rule_list_item_data(country_id, base_env_id, compare_env_id):
    task = RuleSetService.compare_rule_list_rule_set(base_env_id,
                                                     compare_env_id,
                                                     country_id)

    base_env_data = EnvironmentSerializer(Environment.objects.get(id=base_env_id)).data
    compare_env_data = EnvironmentSerializer(Environment.objects.get(id=compare_env_id)).data
    country_data = CountrySerializer(Country.objects.get(id=country_id)).data
    add_list = RuleListItemSerializer(task.get_add_rule_list(), many=True).data
    remove_list = RuleListItemSerializer(task.get_remove_rule_list(), many=True).data
    normal_list = RuleListItemSerializer(task.get_normal_rule_list(), many=True).data
    modify_list = RuleListItemSerializer(task.get_modify_rule_list(), many=True).data

    data = {key.COMPARE_RULE_LIST_COUNTRY: country_data,
            key.COMPARE_RULE_BASE_ENV: base_env_data,
            key.COMPARE_RULE_COMPARE_ENV: compare_env_data,
            key.COMPARE_RULE_COMPARE_HASH_KEY: task.compare_hash_key,
            key.COMPARE_RULE_COMPARE_ADD_LIST: add_list,
            key.COMPARE_RULE_COMPARE_REMOVE_LIST: remove_list,
            key.COMPARE_RULE_COMPARE_NORMAL_LIST: normal_list,
            key.COMPARE_RULE_COMPARE_MODIFY_LIST: modify_list}
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
    pass


def git_sync_branch(request, branch):
    test_git_manager = GitManager(settings.RULESET_GIT_TESTING_BRANCH, 'master')
    if test_git_manager.status == GitManager.STATUS_NEED_PULL:
        test_git_manager.pull()
