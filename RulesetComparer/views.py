import os
import traceback
import re

from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.utils import json
from RulesetComparer.models import Country, Environment, Module, ReportSchedulerInfo, MailContentType
from RulesetComparer.properties import config
from RulesetComparer.properties import dataKey as key
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, RuleSerializer, \
    ModifiedRuleValueSerializer, ModuleSerializer, MailContentTypeSerializer
from RulesetComparer.services import services, rulesetSyncUpService
from RulesetComparer.utils import fileManager, timeUtil
from RulesetComparer.utils.mailSender import MailSender

from RulesetComparer.dataModel.dataBuilder.responseBuilder import ResponseBuilder
from RulesetComparer.dataModel.dataBuilder.reportSchedulerInfoBuilder import ReportSchedulerInfoBuilder
from RulesetComparer.dataModel.dataBuilder.adminConsoleInfoBuilder import AdminConsoleInfoBuilder
from RulesetComparer.utils.logger import *

REQUEST_GET = 'GET'
REQUEST_POST = 'POST'


# admin console page
def admin_console_page(request):
    return render(request, "admin_console_base.html")


def admin_console_server_log_page(request, log_type=None):
    try:
        if log_type is None:
            log_type = DEFAULT_LOG_TYPE

        info_data = AdminConsoleInfoBuilder().get_data()
        log_dir = settings.BASE_DIR + get_file_path("server_log")
        log_file_name = LOG_TYPE_FILE[log_type]
        full_name = log_dir + "/" + log_file_name

        if fileManager.is_file_exist(full_name) is False:
            info_log("views.admin_console_server_log_page", "init info message")
            warning_log("views.admin_console_server_log_page", "init warning message")
            error_log("init error message")

        file = fileManager.load_file(full_name)
        file_secure = re.sub("password</ns0:name><ns0:value>[^<]+</ns0:value>",
                             "password</ns0:name><ns0:value>****</ns0:value>", file.read())
        file_content = file_secure.split("\n")

        data = {
            key.ADMIN_CONSOLE_INFO: info_data,
            key.LOG_TYPE_KEY: log_type,
            key.LOG_TYPE: log_file_name,
            key.LOG_CONTENT: file_content
        }
        return render(request, "server_log.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def admin_console_scheduler_list_page(request):
    try:
        info_data = AdminConsoleInfoBuilder().get_data()
        scheduler_info_list = ReportSchedulerInfo.objects.all()
        data_list = list()
        for scheduler_info in scheduler_info_list:
            data_builder = ReportSchedulerInfoBuilder(scheduler_info)
            data_list.append(data_builder.get_data())

        data = {key.ADMIN_CONSOLE_INFO: info_data,
                key.SCHEDULER_LIST: data_list}

        return render(request, "scheduler_list.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def admin_console_scheduler_create_page(request):
    try:
        environment_list_data = EnvironmentSerializer(Environment.objects.all(), many=True).data
        country_list_data = CountrySerializer(Country.objects.all(), many=True).data
        mail_content_types = MailContentTypeSerializer(MailContentType.objects.all(), many=True).data
        info_data = AdminConsoleInfoBuilder().get_data()

        data = {key.ENVIRONMENT_SELECT_ENVIRONMENT: environment_list_data,
                key.ENVIRONMENT_SELECT_COUNTRY: country_list_data,
                key.RULESET_MAIL_CONTENT_TYPE: mail_content_types,
                key.ADMIN_CONSOLE_INFO: info_data}
        return render(request, "scheduler_create.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def admin_console_scheduler_update_page(request, scheduler_id):
    try:
        environment_list_data = EnvironmentSerializer(Environment.objects.all(), many=True).data
        country_list_data = CountrySerializer(Country.objects.all(), many=True).data
        mail_content_types = MailContentTypeSerializer(MailContentType.objects.all(), many=True).data
        info_data = AdminConsoleInfoBuilder().get_data()

        scheduler_info = ReportSchedulerInfo.objects.get(id=scheduler_id)
        scheduler_data = ReportSchedulerInfoBuilder(scheduler_info).get_data()

        data = {
            key.ENVIRONMENT_SELECT_ENVIRONMENT: environment_list_data,
            key.ENVIRONMENT_SELECT_COUNTRY: country_list_data,
            key.RULESET_MAIL_CONTENT_TYPE: mail_content_types,
            key.ADMIN_CONSOLE_INFO: info_data,
            key.SCHEDULER_DATA: scheduler_data
        }
        return render(request, "scheduler_update.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# ruleset page
def rule_download_page(request):
    try:
        country_list = Country.objects.all()
        environment_list = Environment.objects.all()

        response = {key.ENVIRONMENT_SELECT_COUNTRY: CountrySerializer(country_list, many=True).data,
                    key.ENVIRONMENT_SELECT_ENVIRONMENT: EnvironmentSerializer(environment_list, many=True).data}

        if request.method == REQUEST_POST:
            request_json = get_post_request_json(request)
            info_log("API", "filter rule names, request json =" + str(request_json))
            filtered_rule_names = services.get_filtered_ruleset_list(request_json)
            return render(request, "rule_download_table.html", {key.RULE_NAME_LIST: filtered_rule_names})
        else:
            return render(request, "rule_download.html", response)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def environment_select_page(request):
    try:
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
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def rule_detail_page(request, environment_id, compare_key, rule_name):
    try:
        result_data = fileManager.load_compare_result_file(compare_key)
        environment = Environment.objects.get(id=environment_id)
        detail_rules_data = result_data[key.COMPARE_RESULT_DETAIL_DATA]
        country_data = result_data[key.COMPARE_RULE_LIST_COUNTRY]

        rule_data = detail_rules_data[rule_name]
        # add format to value and expression column
        rules_data = RuleSerializer(rule_data, many=True).data

        data = {key.RULE_KEY_ENVIRONMENT_NAME: environment.name,
                key.RULE_KEY_ENVIRONMENT_ID: environment.id,
                key.RULE_KEY_COUNTRY_NAME: country_data[key.COUNTRY_KEY_NAME],
                key.RULE_KEY_COUNTRY_ID: country_data[key.COUNTRY_KEY_ID],
                key.RULE_KEY_COMPARE_HASH_KEY: compare_key,
                key.RULE_KEY_RULE_NAME: rule_name,
                key.RULE_KEY_RULE_DATA: rules_data}
        return render(request, "rule_show_detail.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def rule_diff_page(request, compare_key, rule_name):
    try:
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
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# api
def send_mail(request, compare_key):
    try:
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
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def download_rulesets(request):
    try:
        request_json = get_post_request_json(request)
        zip_file_path = services.download_rulesets(request_json)
        download_file_name = timeUtil.get_format_current_time(config.TIME_FORMAT.get("year_month_date")) + "_ruleset"

        if os.path.exists(zip_file_path):
            with open(zip_file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                response['Content-Disposition'] = 'attachment; filename="' + download_file_name + '.zip"'
                return response
        raise Http404
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def download_compare_report(request, compare_key):
    try:
        file_path = fileManager.get_compare_result_full_file_name("_html", compare_key)
        data = fileManager.load_compare_result_file(compare_key)
        file_name = data[key.COMPARE_RESULT_LIST_DATA][key.COMPARE_RESULT_DATE_TIME] + "_report"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/html")
                response['Content-Disposition'] = 'attachment; filename="' + file_name + '.html"'
                return response
        raise Http404
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def compare_rule_list_item_data(country_id, base_env_id, compare_env_id):
    try:
        task = services.compare_rule_list_rule_set(base_env_id,
                                                   compare_env_id,
                                                   country_id)

        result_data = fileManager.load_compare_result_file(task.compare_hash_key)
        base_env_data = result_data[key.COMPARE_RULE_BASE_ENV]
        compare_env_data = result_data[key.COMPARE_RULE_COMPARE_ENV]
        country_data = result_data[key.COMPARE_RULE_LIST_COUNTRY]

        list_data = result_data[key.COMPARE_RESULT_LIST_DATA]
        list_data[key.COMPARE_RULE_LIST_COUNTRY] = country_data
        list_data[key.COMPARE_RULE_BASE_ENV] = base_env_data
        list_data[key.COMPARE_RULE_COMPARE_ENV] = compare_env_data
        return list_data
    except Exception:
        error_log(traceback.format_exc())
        return []


def get_module_list(request):
    module_list = ModuleSerializer(Module.objects.all(), many=True)
    result = ResponseBuilder(data=module_list.data).get_data()
    return JsonResponse(result.get_data())


def create_module(request):
    request_json = get_post_request_json(request)
    serializer = ModuleSerializer(data=request_json)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def get_scheduler_list(request):
    try:
        scheduler_info_list = ReportSchedulerInfo.objects.all()
        data_list = list()
        for scheduler_info in scheduler_info_list:
            data_builder = ReportSchedulerInfoBuilder(scheduler_info)
            data_list.append(data_builder.get_data())
        result = ResponseBuilder(data=data_list).get_data()
        response = JsonResponse(data=result)
        return response
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def get_scheduler(request, scheduler_id):
    try:
        scheduler_info = ReportSchedulerInfo.objects.get(id=scheduler_id)
        scheduler_data = ReportSchedulerInfoBuilder(scheduler_info).get_data()
        result = ResponseBuilder(data=scheduler_data).get_data()
        response = JsonResponse(data=result)
        return response
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def create_scheduler(request):
    try:
        request_json = get_post_request_json(request)
        info_log("API", "create_scheduler, request json =" + str(request_json))
        scheduler_info = services.create_report_scheduler(request_json)
        info_data = ReportSchedulerInfoBuilder(scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def update_scheduler(request):
    try:
        request_json = get_post_request_json(request)
        info_log("API", "update_scheduler, request json =" + str(request_json))
        scheduler_info = services.update_report_scheduler(request_json)
        info_data = ReportSchedulerInfoBuilder(scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def delete_scheduler(request):
    try:
        request_json = get_post_request_json(request)
        task_id = request_json["id"]
        services.delete_scheduler(task_id)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def sync_up_ruleset(request):
    try:
        request_json = get_post_request_json(request)
        rulesetSyncUpService.sync_up_rulesets_test(request_json)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def create_ruleset(request):
    try:
        rulesetSyncUpService.create_ruleset_test()
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def update_ruleset(request):
    try:
        rulesetSyncUpService.update_ruleset_test()
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# todo : return json rule list response
def json_rule_list(request, environment, country):
    response_model = services.get_rule_list_from_b2b(environment, country)
    return response_model.get_response_json()


# todo : return json rule detail
def json_rule_detail(request, country, env, rule_set_name):
    pass


# todo : return json rule diff result
def json_rule_diff(request, base_env_id, compare_env_id, country_id, compare_key):
    pass


def get_post_request_json(request):
    if request.method != REQUEST_POST:
        return HttpResponseBadRequest
    else:
        try:
            request_json = json.loads(request.body.decode())
            return request_json
        except BaseException:
            error_log(traceback.format_exc())
