from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from RulesetComparer.models import B2BRuleSetServer, Country, Environment
from RulesetComparer.properties import dataKey as key
from RulesetComparer.properties import config
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, RuleListItemSerializer
from RulesetComparer.serializers.serializers import RuleSerializer, ModifiedRuleValueSerializer
from RulesetComparer.services.services import RuleSetService
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.mailSender import MailSender

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


def rule_detail(request, compare_key, rule_name):
    compare_result_data = fileManager.load_compare_result_file(compare_key)
    rule_detail_map = compare_result_data[key.COMPARE_RESULT_DETAIL_DATA]
    rule_json = rule_detail_map[rule_name]
    rules_data = RuleSerializer(rule_json, many=True).data
    data = {key.RULE_KEY_RULE_NAME: rule_name,
            key.RULE_KEY_RULE_DATA: rules_data}
    return render(request, "rule_show_detail.html", data)


def rule_diff(request, base_env_id, compare_env_id, compare_key, rule_name):
    compare_result_data = fileManager.load_compare_result_file(compare_key)
    rule_diff_map = compare_result_data[key.COMPARE_RESULT_DIFF_DATA]
    rule_json = rule_diff_map[rule_name]
    base_env = Environment.objects.get(id=base_env_id)
    compare_env = Environment.objects.get(id=compare_env_id)
    add_list = RuleSerializer(rule_json[key.RULE_LIST_ITEM_TABLE_TYPE_ADD], many=True).data
    remove_list = RuleSerializer(rule_json[key.RULE_LIST_ITEM_TABLE_TYPE_REMOVE], many=True).data
    modify_list = ModifiedRuleValueSerializer(rule_json[key.RULE_LIST_ITEM_TABLE_TYPE_MODIFY], many=True).data
    normal_list = RuleSerializer(rule_json[key.RULE_LIST_ITEM_TABLE_TYPE_NORMAL], many=True).data

    data = {
        key.RULE_KEY_RULE_NAME: rule_name,
        key.RULE_DIFF_KEY_BASE_ENV_NAME: base_env.name,
        key.RULE_DIFF_KEY_COMPARED_ENV_NAME: compare_env.name,
        key.RULE_DIFF_KEY_ADD_LIST: add_list,
        key.RULE_DIFF_KEY_REMOVE_LIST: remove_list,
        key.RULE_DIFF_KEY_MODIFY_LIST: modify_list,
        key.RULE_DIFF_KEY_NORMAL_LIST: normal_list
    }
    return render(request, "rule_show_diff.html", data)


def send_mail_test(request, compare_key):
    mail_sender = MailSender(config.SEND_COMPARE_RESULT_MAIL)
    mail_sender.compose_msg()

    file_path = fileManager.get_compare_result_full_file_name("_html", compare_key)
    file_name = "test_report.html"
    application = "text"
    mail_sender.add_attachment(file_path, file_name, application)

    mail_sender.send()
    mail_sender.quit()


def generate_compare_result_html(request, compare_key):
    data = fileManager.load_compare_result_file(compare_key)
    template = get_template("rule_item_list.html")
    html = template.render(data)
    fileManager.save_compare_result_html(compare_key, html)
    return HttpResponse(html, content_type='text/html')


def compare_rule_list_item_data(country_id, base_env_id, compare_env_id):
    task = RuleSetService.compare_rule_list_rule_set(base_env_id,
                                                     compare_env_id,
                                                     country_id)

    compare_result_data = fileManager.load_compare_result_file(task.compare_hash_key)
    list_data_map = compare_result_data[key.COMPARE_RESULT_LIST_DATA]
    base_env_data = EnvironmentSerializer(Environment.objects.get(id=base_env_id)).data
    compare_env_data = EnvironmentSerializer(Environment.objects.get(id=compare_env_id)).data
    country_data = CountrySerializer(Country.objects.get(id=country_id)).data

    add_list = RuleListItemSerializer(list_data_map[key.COMPARE_RESULT_ADD_LIST], many=True).data
    remove_list = RuleListItemSerializer(list_data_map[key.COMPARE_RESULT_REMOVE_LIST], many=True).data
    normal_list = RuleListItemSerializer(list_data_map[key.COMPARE_RESULT_NORMAL_LIST], many=True).data
    modify_list = RuleListItemSerializer(list_data_map[key.COMPARE_RESULT_MODIFY_LIST], many=True).data

    compare_list_data = {key.COMPARE_RULE_LIST_COUNTRY: country_data,
                         key.COMPARE_RULE_BASE_ENV: base_env_data,
                         key.COMPARE_RULE_COMPARE_ENV: compare_env_data,
                         key.COMPARE_RULE_COMPARE_HASH_KEY: task.compare_hash_key,
                         key.COMPARE_RESULT_ADD_LIST: add_list,
                         key.COMPARE_RESULT_REMOVE_LIST: remove_list,
                         key.COMPARE_RESULT_NORMAL_LIST: normal_list,
                         key.COMPARE_RESULT_MODIFY_LIST: modify_list}
    return compare_list_data


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
