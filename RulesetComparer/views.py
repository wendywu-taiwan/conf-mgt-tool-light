import os
import traceback
import re

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.utils import json

from RulesetComparer.date_model.json_builder.sync_scheduler_create_page import SyncSchedulerCreatePageBuilder
from RulesetComparer.date_model.json_builder.sync_scheduler_update_page import SyncSchedulerUpdatePageBuilder
from permission.utils.page_visibility import *
from permission.utils.permission_manager import enable_environments, enable_countries
from common.utils.utility import get_union, contains
from RulesetComparer.date_model.json_parser.create_ruleset_sync_scheduler import CreateRulesetSyncSchedulerParser
from RulesetComparer.models import Country, Module, RulesetSyncUpScheduler
from RulesetComparer.utils.threadManager import *
from RulesetComparer.properties import config
from RulesetComparer.properties import key as key
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer, \
    ModuleSerializer
from RulesetComparer.services import services, sync, recover, log
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.properties.message import *

from RulesetComparer.date_model.json_builder.response import ResponseBuilder
from RulesetComparer.date_model.json_builder.report_scheduler_info import ReportSchedulerInfoBuilder
from RulesetComparer.date_model.json_builder.ruleset_sync_scheduler import RulesetSyncSchedulerBuilder, \
    RulesetSyncSchedulersBuilder
from RulesetComparer.date_model.json_builder.ruleset_download_page import RulesetDownloadPageBuilder
from RulesetComparer.date_model.json_builder.admin_console_info import AdminConsoleInfoBuilder
from RulesetComparer.date_model.json_builder.environment import EnvironmentBuilder
from RulesetComparer.date_model.json_builder.country import CountryBuilder, CountriesBuilder
from RulesetComparer.properties.status_code import *
from common.data_object.error.PermissionDeniedError import PermissionDeniedError
from permission.utils.permission_manager import check_function_visibility, enable_environments_data
from RulesetComparer.services.services import *
from RulesetComparer.services.report_scheduler import *


######################################## Admin Console ########################################
def permission_check(request, check_visibility, get_visible_data, executor):
    try:
        check_visibility()
        return executor(get_visible_data())
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# admin console page
@login_required
def admin_console_page(request):
    data = {KEY_NAVIGATION_INFO: AdminConsoleInfoBuilder(request.user).get_data()}
    return render(request, "admin_console_base.html", data)


@login_required
def admin_console_server_log_page(request, log_type=None):
    def check_visibility():
        check_function_visibility(request, KEY_F_SERVER_LOG)

    def get_visible_data():
        pass

    def after_check(visible_data):
        check_function_visibility(request, KEY_F_SERVER_LOG)
        data = server_log_page(request.user, log_type)
        return render(request, "server_log.html", data)

    return permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_report_scheduler_list_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_REPORT_TASK)

    def get_visible_data():
        return ReportSchedulerInfo.objects.get_visible_schedulers(request.user.id)

    def after_check(visible_data):
        data = ReportSchedulersBuilder(request.user, visible_data).get_data()
        return render(request, "scheduler_list.html", data)

    return permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_report_scheduler_create_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_REPORT_TASK)

    def get_visible_data():
        environments = enable_environments_data(request.user.id)
        return environments

    def after_check(visible_data):
        data = ReportSchedulerCreatePageBuilder(request.user, visible_data).get_data()
        return render(request, "scheduler_create.html", data)

    return permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_report_scheduler_update_page(request, scheduler_id):
    def check_visibility():
        check_function_visibility(request, KEY_F_REPORT_TASK)
        scheduler = ReportSchedulerInfo.objects.get(id=scheduler_id)
        check_scheduler_detail_visibility(request.user.id,
                                          scheduler.base_environment.id,
                                          scheduler.compare_environment.id,
                                          scheduler.country_list.all(),
                                          KEY_F_REPORT_TASK)

    def get_visible_data():
        environments = enable_environments_data(request.user.id)
        return environments

    def after_check(visible_data):
        data = ReportSchedulerUpdatePageBuilder(request.user, visible_data, scheduler_id).get_data()
        return render(request, "report_scheduler_update.html", data)

    return permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_sync_scheduler_list_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_AUTO_SYNC_TASK)

    def get_visible_data():
        environment_list = enable_environments(request.user.id)
        return RulesetSyncUpScheduler.objects.filter_environments_and_countries(request.user.id, environment_list)

    def after_check(visible_data):
        data = RulesetSyncSchedulersBuilder(request.user, visible_data).get_data()
        return render(request, "sync_scheduler_list.html", data)

    return permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_sync_scheduler_create_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_AUTO_SYNC_TASK)
        enable_environment_list = enable_environments(request.user.id)
        git_environment = Environment.objects.get(name=GIT_NAME)
        int2_environment = Environment.objects.get(name=INT2_NAME)
        # check data visibility
        if not contains(enable_environment_list, int2_environment.id) or \
                not contains(enable_environment_list, git_environment.id):
            raise PermissionDeniedError

    def get_visible_data():
        pass

    def after_check(visible_data):
        data = SyncSchedulerCreatePageBuilder(request.user).get_data()
        return render(request, "sync_scheduler_create.html", data)

    return permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_sync_scheduler_update_page(request, scheduler_id):
    def check_visibility():
        check_function_visibility(request, KEY_F_AUTO_SYNC_TASK)
        scheduler = RulesetSyncUpScheduler.objects.get(id=scheduler_id)
        check_scheduler_detail_visibility(request.user.id,
                                          scheduler.source_environment.id,
                                          scheduler.target_environment.id,
                                          scheduler.country_list.all(),
                                          KEY_F_AUTO_SYNC_TASK)

    def get_visible_data():
        pass

    def after_check(visible_data):
        data = SyncSchedulerUpdatePageBuilder(request.user, scheduler_id).get_data()
        return render(request, "sync_scheduler_update.html", data)

    return permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_recover_ruleset_filtered_page(request):
    try:
        check_function_visibility(request, KEY_F_RECOVERY)

        environment_list = recover.filter_environment()
        enable_environment_list = enable_environments(request.user.id)
        union_list = get_union(environment_list, enable_environment_list)

        array = []
        for environment_id in union_list:
            array.append(EnvironmentBuilder(id=environment_id).get_data())

        data = {
            key.KEY_ENVIRONMENTS: array
        }
        data = add_navigation_information(request, data)
        return render(request, "recovery.html", data)
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


@login_required
def admin_console_recover_ruleset_filtered_environment_page(request):
    try:
        check_function_visibility(request, KEY_F_RECOVERY)

        request_json = get_post_request_json(request)
        environment_id = request_json.get(key.RULE_KEY_ENVIRONMENT_ID)
        countries = recover.filter_country(environment_id)
        # check data visibility
        enable_country_list = enable_countries(request.user.id, environment_id)
        union_list = get_union(countries, enable_country_list)

        array = []
        for country_id in union_list:
            country = Country.objects.get(id=country_id)
            array.append(CountryBuilder(country).get_data())

        data = {
            key.KEY_COUNTRIES: array
        }
        data = add_navigation_information(request, data)
        return render(request, "select_country_dropdown.html", data)
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


@login_required
def admin_console_recover_ruleset_backup_list_page(request):
    try:
        check_function_visibility(request, KEY_F_RECOVERY)

        request_json = get_post_request_json(request)
        result_data = recover.filter_backup_list(request_json)
        result_data = add_navigation_information(request, result_data)
        return render(request, "backup_data_view.html", result_data)
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


#  entrance for ruleset log list page init
@login_required
def admin_console_ruleset_log_list_page(request):
    try:
        check_function_visibility(request, KEY_F_RULESET_LOG)

        request_json = get_post_request_json(request)
        result_data = log.get_ruleset_log_list(request.user, request_json, False)
        result_data = add_navigation_information(request, result_data)
        return render(request, "ruleset_log.html", result_data)
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


#  entrance for ruleset log list filter change
@login_required
def admin_console_ruleset_log_list_filter_page(request):
    try:
        check_function_visibility(request, KEY_F_RULESET_LOG)

        request_json = get_post_request_json(request)
        result_data = log.get_ruleset_log_list(request.user, request_json, True)
        result_data = add_navigation_information(request, result_data)
        return render(request, "ruleset_log_list.html", result_data)
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# entrance for ruleset log list page change
@login_required
def admin_console_ruleset_log_list_page_change(request):
    try:
        check_function_visibility(request, KEY_F_RULESET_LOG)

        request_json = get_post_request_json(request)
        result_data = log.get_ruleset_log_list(request.user, request_json, False)
        result_data = add_navigation_information(request, result_data)
        return render(request, "ruleset_log_list.html", result_data)
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


@login_required
def admin_console_ruleset_log_detail_page(request, log_id):
    try:
        check_function_visibility(request, KEY_F_RULESET_LOG)
        check_ruleset_log_detail_visibility(request.user.id, log_id)

        result = {KEY_LOG_DATA: log.get_ruleset_log_detail(request.user, log_id)}
        result = add_navigation_information(request, result)
        return render(request, "ruleset_log_detail.html", result)
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def add_navigation_information(request, result):
    info_data = AdminConsoleInfoBuilder(request.user).get_data()
    result[ADMIN_CONSOLE_INFO] = info_data
    return result


######################################## Frontend ########################################

# ruleset page
def rule_download_page(request):
    try:
        page_data = RulesetDownloadPageBuilder().get_data()
        return render(request, "rule_download.html", page_data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# ruleset page
def rule_download_filter_page(request):
    try:
        request_json = get_post_request_json(request)
        result_data = services.get_filtered_ruleset_page_data(request_json)
        return render(request, "rule_download_table.html", result_data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def environment_select_page(request):
    try:
        country_list = Country.objects.all()
        environment_list = Environment.objects.filter(active=1)

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


def ruleset_detail_page(request, environment_id, country_id, ruleset_name, compare_key=None):
    try:
        data = services.ruleset_detail_page_data(environment_id, country_id, ruleset_name, compare_key)
        return render(request, "rule_show_detail.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def ruleset_detail_backup_page(request, backup_key, backup_folder, ruleset_name):
    try:
        data = services.ruleset_detail_backup_page_data(backup_key, backup_folder, ruleset_name)
        return render(request, "rule_show_detail.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def ruleset_diff_page(request, compare_key, ruleset_name):
    try:
        data = services.ruleset_diff_compare_result(compare_key, ruleset_name)
        if data[RULE_DIFF_HAS_CHANGES] is False:
            result = ResponseBuilder(status_code=COMPARE_NO_CHANGES).get_data()
            return JsonResponse(result)
        else:
            return render(request, "rule_show_diff.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=INTERNAL_SERVER_ERROR, message="Internal Server Error").get_data()
        return JsonResponse(result)


def ruleset_diff_backup_page(request, backup_key, ruleset_name):
    try:
        data = services.ruleset_diff_backup(backup_key, ruleset_name)
        if data[RULE_DIFF_HAS_CHANGES] is False:
            result = ResponseBuilder(status_code=COMPARE_NO_CHANGES).get_data()
            return JsonResponse(result)
        else:
            return render(request, "rule_show_diff.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=INTERNAL_SERVER_ERROR, message="Internal Server Error").get_data()
        return JsonResponse(result)


def ruleset_diff_backup_with_server_page(request, backup_key, backup_folder, ruleset_name):
    try:
        data = services.ruleset_diff_backup_with_server(backup_key, backup_folder, ruleset_name)
        if data[RULE_DIFF_HAS_CHANGES] is False:
            result = ResponseBuilder(status_code=COMPARE_NO_CHANGES).get_data()
            return JsonResponse(result)
        else:
            return render(request, "rule_show_diff.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=INTERNAL_SERVER_ERROR, message="Internal Server Error").get_data()
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


# recovery - apply ruleset
def recover_rulesets(request):
    try:
        request_json = get_post_request_json(request)
        result_data = sync.sync_up_rulesets_from_backup(request_json, request.user)
        result = ResponseBuilder(data=result_data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# ruleset log detail - apply ruleset
def apply_ruleset_to_server(request):
    try:
        request_json = get_post_request_json(request)
        result_data = sync.sync_up_ruleset_from_backup(request_json, request.user)
        result = ResponseBuilder(data=result_data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=INTERNAL_SERVER_ERROR, message="Internal Server Error").get_data()
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
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def get_module_list(request):
    module_list = ModuleSerializer(Module.objects.all(), many=True)
    result = ResponseBuilder(data=module_list.data).get_data()
    return JsonResponse(result.get_data())


def create_module(request):
    request_json = get_post_request_json(request)
    serializer = ModuleSerializer(data=request_json)
    serializer.is_valid(raise_exception=True)
    serializer.save()


# rulesets report job
def get_rulesets_report_job(request, scheduler_id):
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


def get_rulesets_report_jobs(request):
    try:
        schedulers = report_scheduler.get_schedulers()
        data_list = list()
        for scheduler in schedulers:
            data_builder = ReportSchedulerInfoBuilder(scheduler)
            data_list.append(data_builder.get_data())
        result = ResponseBuilder(data=data_list).get_data()
        response = JsonResponse(data=result)
        return response
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def create_ruleset_report_job(request):
    try:
        request_json = get_post_request_json(request)
        info_log("API", "create_scheduler, request json =" + str(request_json))
        scheduler_info = report_scheduler.create_scheduler(request_json, request.user)
        info_data = ReportSchedulerInfoBuilder(request.user, scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def update_ruleset_report_job(request):
    try:
        request_json = get_post_request_json(request)
        info_log("API", "update_scheduler, request json =" + str(request_json))
        scheduler_info = report_scheduler.update_report_scheduler(request_json, request.user)
        info_data = ReportSchedulerInfoBuilder(request.user, scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def update_rulesets_report_status(request):
    try:
        request_json = get_post_request_json(request)
        scheduler = report_scheduler.update_scheduler_status(request_json, request.user)
        data = ReportSchedulerInfoBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def delete_ruleset_report_job(request):
    try:
        request_json = get_post_request_json(request)
        report_scheduler.delete_scheduler(request_json, request.user)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


# ruleset sync job
def get_rulesets_sync_jobs(request):
    try:
        schedulers = sync_scheduler.get_schedulers()
        data_list = list()
        for scheduler in schedulers:
            data_builder = RulesetSyncSchedulerBuilder(scheduler)
            data_list.append(data_builder.get_data())

        result = ResponseBuilder(data=data_list).get_data()
        response = JsonResponse(data=result)
        return response
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def run_rulesets_sync_job(request):
    try:
        request_json = get_post_request_json(request)
        parser = CreateRulesetSyncSchedulerParser(request_json, request.user)
        run_in_background(sync.sync_up_rulesets_without_scheduler, parser)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def create_rulesets_sync_job(request):
    try:
        request_json = get_post_request_json(request)
        scheduler = sync_scheduler.create_scheduler(request_json, request.user)
        data = RulesetSyncSchedulerBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def update_rulesets_sync_job(request):
    try:
        request_json = get_post_request_json(request)
        scheduler = sync_scheduler.update_scheduler(request_json, request.user)
        data = RulesetSyncSchedulerBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def update_rulesets_sync_job_status(request):
    try:
        request_json = get_post_request_json(request)
        scheduler = sync_scheduler.update_scheduler_status(request_json, request.user)
        data = RulesetSyncSchedulerBuilder(scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def delete_rulesets_sync_job(request):
    try:
        request_json = get_post_request_json(request)
        sync_scheduler.delete_scheduler(request_json, request.user)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)
    except PermissionDeniedError:
        result = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def create_ruleset(request):
    try:
        sync.create_ruleset_test()
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def update_ruleset(request):
    try:
        sync.update_ruleset_test()
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def compare_ruleset_test(request):
    try:
        pass
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def get_ruleset(request):
    try:
        request_json = get_post_request_json(request)
        ruleset = log.get_ruleset(request_json)
        result = {KEY_RULESET_DATA: ruleset}
        return render(request, "ruleset_content_view.html", result)
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
