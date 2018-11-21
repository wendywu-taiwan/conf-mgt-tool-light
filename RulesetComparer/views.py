import os
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from RulesetComparer.models import Country, Environment
from RulesetComparer.properties import dataKey as key
from RulesetComparer.properties import config
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, RuleListItemSerializer, \
    RuleSerializer, ModifiedRuleValueSerializer
from RulesetComparer.services.services import RuleSetService
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.services.initDataService import InitDataService

REQUEST_GET = 'GET'
REQUEST_POST = 'POST'


def environment_select(request):
    InitDataService()

    country_list = Country.objects.all()
    environment_list = Environment.objects.all()

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


def rule_detail(request, environment_name, compare_key, rule_name):
    result_data = fileManager.load_compare_result_file(compare_key)
    detail_rules_data = result_data[key.COMPARE_RESULT_DETAIL_DATA]

    rule_data = detail_rules_data[rule_name]
    # add format to value and expression column
    rules_data = RuleSerializer(rule_data, many=True).data

    data = {key.RULE_KEY_ENVIRONMENT: environment_name,
            key.RULE_KEY_RULE_NAME: rule_name,
            key.RULE_KEY_RULE_DATA: rules_data}
    return render(request, "rule_show_detail.html", data)


def rule_diff(request, compare_key, rule_name):
    result_data = fileManager.load_compare_result_file(compare_key)
    base_env = result_data[key.COMPARE_RULE_BASE_ENV]
    compare_env = result_data[key.COMPARE_RULE_COMPARE_ENV]

    diff_rules_data = result_data[key.COMPARE_RESULT_DIFF_DATA]
    rule_data = diff_rules_data[rule_name]

    add_list = RuleSerializer(rule_data[key.RULE_LIST_ITEM_TABLE_TYPE_ADD], many=True).data
    remove_list = RuleSerializer(rule_data[key.RULE_LIST_ITEM_TABLE_TYPE_REMOVE], many=True).data
    modify_list = ModifiedRuleValueSerializer(rule_data[key.RULE_LIST_ITEM_TABLE_TYPE_MODIFY], many=True).data
    normal_list = RuleSerializer(rule_data[key.RULE_LIST_ITEM_TABLE_TYPE_NORMAL], many=True).data

    data = {
        key.RULE_KEY_RULE_NAME: rule_name,
        key.RULE_DIFF_KEY_BASE_ENV_NAME: base_env["name"],
        key.RULE_DIFF_KEY_COMPARED_ENV_NAME: compare_env["name"],
        key.RULE_DIFF_KEY_ADD_LIST: add_list,
        key.RULE_DIFF_KEY_REMOVE_LIST: remove_list,
        key.RULE_DIFF_KEY_MODIFY_LIST: modify_list,
        key.RULE_DIFF_KEY_NORMAL_LIST: normal_list
    }
    return render(request, "rule_show_diff.html", data)


def send_mail(request, compare_key):
    result_data = fileManager.load_compare_result_file(compare_key)
    list_data = result_data[key.COMPARE_RESULT_LIST_DATA]
    list_data[key.COMPARE_RULE_BASE_ENV] = result_data[key.COMPARE_RULE_BASE_ENV]
    list_data[key.COMPARE_RULE_COMPARE_ENV] = result_data[key.COMPARE_RULE_COMPARE_ENV]
    html_content = render_to_string('compare_info_mail_content.html', list_data)

    mail_sender = MailSender(config.SEND_COMPARE_RESULT_MAIL)
    mail_sender.compose_msg(None, None, html_content)

    file_path = fileManager.get_compare_result_full_file_name("_html", compare_key)
    file_name = "test_report.html"
    application = "text"
    mail_sender.add_attachment(file_path, file_name, application)

    mail_sender.send()
    mail_sender.quit()

    response = HttpResponse()
    return response


def download_compare_report(request, compare_key):
    file_path = fileManager.get_compare_result_full_file_name("_html", compare_key)
    data = fileManager.load_compare_result_file(compare_key)
    file_name = data[key.COMPARE_RESULT_LIST_DATA][key.COMPARE_RESULT_DATE_TIME] + "_report"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/html")
            response['Content-Disposition'] = 'attachment; filename="' + file_name + '.html"'
            return response
    raise Http404


def compare_rule_list_item_data(country_id, base_env_id, compare_env_id):
    task = RuleSetService.compare_rule_list_rule_set(base_env_id,
                                                     compare_env_id,
                                                     country_id)

    generate_compare_result_html(task.compare_hash_key)

    result_data = fileManager.load_compare_result_file(task.compare_hash_key)
    base_env_data = result_data[key.COMPARE_RULE_BASE_ENV]
    compare_env_data = result_data[key.COMPARE_RULE_COMPARE_ENV]
    country_data = result_data[key.COMPARE_RULE_LIST_COUNTRY]

    list_data = result_data[key.COMPARE_RESULT_LIST_DATA]
    list_data[key.COMPARE_RULE_LIST_COUNTRY] = country_data
    list_data[key.COMPARE_RULE_BASE_ENV] = base_env_data
    list_data[key.COMPARE_RULE_COMPARE_ENV] = compare_env_data
    return list_data


def generate_compare_result_html(compare_key):
    data = fileManager.load_compare_result_file(compare_key)
    template = get_template("compare_result_report.html")
    html = template.render(data)
    fileManager.save_compare_result_html(compare_key, html)


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
