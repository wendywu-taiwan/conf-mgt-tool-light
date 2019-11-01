import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from common.views import page_permission_check, page_error_check, action_permission_check, action_error_check
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.environment import EnvironmentsBuilder
from common.data_object.json_builder.module import ModulesBuilder
from common.data_object.json_builder.response import ResponseBuilder

from RulesetComparer.date_model.json_builder.recovery_page import RecoveryPageFilterEnvironmentsBuilder, \
    RecoveryPageFilterCountriesBuilder
from RulesetComparer.date_model.json_builder.report_scheduler_create_page import ReportSchedulerCreatePageBuilder
from RulesetComparer.date_model.json_builder.report_scheduler_update_page import ReportSchedulerUpdatePageBuilder
from RulesetComparer.date_model.json_builder.sync_scheduler_create_page import SyncSchedulerCreatePageBuilder
from RulesetComparer.date_model.json_builder.sync_scheduler_update_page import SyncSchedulerUpdatePageBuilder
from permission.utils.page_visibility import *
from permission.utils.permission_manager import enable_environments, enable_countries
from common.utils.utility import get_union, contains
from common.data_object.error.error import PermissionDeniedError
from common.data_object.error.status import *
from RulesetComparer.date_model.json_parser.create_ruleset_sync_scheduler import CreateRulesetSyncSchedulerParser
from RulesetComparer.models import Country, Module, RulesetSyncUpScheduler
from RulesetComparer.utils.threadManager import *
from RulesetComparer.properties import config
from RulesetComparer.properties import key as key
from RulesetComparer.serializers.serializers import ModuleSerializer
from RulesetComparer.services import services, sync, recover, log
from RulesetComparer.utils.mailSender import MailSender
from RulesetComparer.date_model.json_builder.report_scheduler_info import ReportSchedulerInfoBuilder, \
    ReportSchedulersBuilder
from RulesetComparer.date_model.json_builder.ruleset_sync_scheduler import RulesetSyncSchedulerBuilder, \
    RulesetSyncSchedulersBuilder
from RulesetComparer.date_model.json_builder.ruleset_download_page import RulesetDownloadPageBuilder
from RulesetComparer.date_model.json_builder.admin_console_info import AdminConsoleInfoBuilder

from permission.utils.permission_manager import check_function_visibility, enable_environments_data
from RulesetComparer.services.services import *
from RulesetComparer.services.report_scheduler import *


######################################## Admin Console ########################################
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

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_report_scheduler_list_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_REPORT_TASK)

    def get_visible_data():
        return ReportSchedulerInfo.objects.get_visible_schedulers(request.user.id)

    def after_check(visible_data):
        data = ReportSchedulersBuilder(request.user, visible_data).get_data()
        return render(request, "scheduler_list.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


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

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


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

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


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

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


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

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


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

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_recover_ruleset_filtered_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_RECOVERY)

    def get_visible_data():
        environment_list = recover.filter_environment()
        enable_environment_list = enable_environments(request.user.id)
        union_list = get_union(environment_list, enable_environment_list)
        return union_list

    def after_check(visible_data):
        data = RecoveryPageFilterEnvironmentsBuilder(request.user, visible_data).get_data()
        return render(request, "recovery.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_recover_ruleset_filtered_environment_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_RECOVERY)

    def get_visible_data():
        request_json = get_post_request_json(request)
        environment_id = request_json.get(key.RULE_KEY_ENVIRONMENT_ID)
        countries = recover.filter_country(environment_id)
        enable_country_list = enable_countries(request.user.id, environment_id)
        union_list = get_union(countries, enable_country_list)
        return union_list

    def after_check(visible_data):
        data = RecoveryPageFilterCountriesBuilder(request.user, visible_data).get_data()
        return render(request, "select_country_dropdown.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_recover_ruleset_backup_list_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_RECOVERY)

    def get_visible_data():
        pass

    def after_check(visible_data):
        request_json = get_post_request_json(request)
        result_data = recover.filter_backup_list(request.user, request_json)
        return render(request, "backup_data_view.html", result_data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


#  entrance for ruleset log list page init
@login_required
def admin_console_ruleset_log_list_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_RULESET_LOG)

    def get_visible_data():
        pass

    def after_check(visible_data):
        request_json = get_post_request_json(request)
        data = log.get_ruleset_log_list(request.user, request_json, False)
        return render(request, "ruleset_log.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


#  entrance for ruleset log list filter change
@login_required
def admin_console_ruleset_log_list_filter_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_RULESET_LOG)

    def get_visible_data():
        pass

    def after_check(visible_data):
        request_json = get_post_request_json(request)
        data = log.get_ruleset_log_list(request.user, request_json, True)
        return render(request, "ruleset_log_list.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


# entrance for ruleset log list page change
@login_required
def admin_console_ruleset_log_list_page_change(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_RULESET_LOG)

    def get_visible_data():
        pass

    def after_check(visible_data):
        request_json = get_post_request_json(request)
        data = log.get_ruleset_log_list(request.user, request_json, False)
        return render(request, "ruleset_log_list.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_ruleset_log_detail_page(request, log_id):
    def check_visibility():
        check_function_visibility(request, KEY_F_RULESET_LOG)
        check_ruleset_log_detail_visibility(request.user.id, log_id)

    def get_visible_data():
        pass

    def after_check(visible_data):
        data = log.get_ruleset_log_detail(request.user, log_id)
        return render(request, "ruleset_log_detail.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


######################################## Frontend ########################################

# ruleset page
def rule_download_page(request):
    def after_check():
        page_data = RulesetDownloadPageBuilder().get_data()
        return render(request, "rule_download.html", page_data)

    return page_error_check(after_check)


# ruleset page
def rule_download_filter_page(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_data = services.get_filtered_ruleset_page_data(request_json)
        return render(request, "rule_download_table.html", result_data)

    return page_error_check(after_check)


def environment_select_page(request):
    def after_check():
        countries = Country.objects.all()
        environments = Environment.objects.filter(active=1)

        response = {key.ENVIRONMENT_SELECT_COUNTRY: CountriesBuilder(countries=countries).get_data(),
                    key.ENVIRONMENT_SELECT_ENVIRONMENT: EnvironmentsBuilder(environments=environments).get_data()}

        if request.method == REQUEST_GET:
            return render(request, "environment_select.html", response)
        elif request.method == REQUEST_POST:
            country_id = request.POST.get('country')
            base_env_id = request.POST.get('base_env')
            compare_env_id = request.POST.get('compare_env')

            if not country_id or not base_env_id or not compare_env_id or base_env_id == compare_env_id:
                return render(request, "environment_select.html", response)
            else:
                data = services.compare_rule_list_rule_set(base_env_id, compare_env_id, country_id)
                return render(request, "rule_item_list.html", data)

    return page_error_check(after_check)


def ruleset_detail_page(request, environment_id, country_id, ruleset_name, compare_key=None):
    def after_check():
        data = services.ruleset_detail_page_data(environment_id, country_id, ruleset_name, compare_key)
        return render(request, "rule_show_detail.html", data)

    return page_error_check(after_check)


def ruleset_detail_backup_page(request, backup_key, backup_folder, ruleset_name):
    def after_check():
        data = services.ruleset_detail_backup_page_data(backup_key, backup_folder, ruleset_name)
        return render(request, "rule_show_detail.html", data)

    return page_error_check(after_check)


def ruleset_diff_page(request, compare_key, ruleset_name):
    def after_check():
        data = services.ruleset_diff_compare_result(compare_key, ruleset_name)
        if data[KEY_HAS_CHANGES] is False:
            result = ResponseBuilder(status_code=COMPARE_NO_CHANGES).get_data()
            return JsonResponse(result)
        else:
            return render(request, "rule_show_diff.html", data)

    return page_error_check(after_check)


def ruleset_diff_backup_page(request, backup_key, ruleset_name):
    def after_check():
        data = services.ruleset_diff_backup(backup_key, ruleset_name)
        if data[KEY_HAS_CHANGES] is False:
            result = ResponseBuilder(status_code=COMPARE_NO_CHANGES).get_data()
            return JsonResponse(result)
        else:
            return render(request, "rule_show_diff.html", data)

    return page_error_check(after_check)


def ruleset_diff_backup_with_server_page(request, backup_key, backup_folder, ruleset_name):
    def after_check():
        data = services.ruleset_diff_backup_with_server(backup_key, backup_folder, ruleset_name)
        if data[KEY_HAS_CHANGES] is False:
            result = ResponseBuilder(status_code=COMPARE_NO_CHANGES).get_data()
            return JsonResponse(result)
        else:
            return render(request, "rule_show_diff.html", data)

    return page_error_check(after_check)


# api
def send_mail(request, compare_key):
    def after_check():
        result_data = fileManager.load_compare_result_file(compare_key)
        list_data = result_data[key.COMPARE_RESULT_LIST_DATA]
        list_data[key.KEY_BASE_ENV] = result_data[key.KEY_BASE_ENV]
        list_data[key.KEY_COMPARE_ENV] = result_data[key.KEY_COMPARE_ENV]
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

    return action_error_check(after_check)


def download_rulesets(request):
    def after_check():
        request_json = get_post_request_json(request)
        zip_file_path = services.download_rulesets(request_json)

        if os.path.exists(zip_file_path):
            with open(zip_file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                return response
        raise Http404

    return action_error_check(after_check)


def download_compare_report(request, compare_key):
    def after_check():
        file_path = fileManager.get_compare_result_full_file_name("_html", compare_key)
        data = fileManager.load_compare_result_file(compare_key)
        file_name = data[key.COMPARE_RESULT_LIST_DATA][key.COMPARE_RESULT_DATE_TIME] + "_report"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/html")
                response['Content-Disposition'] = 'attachment; filename="' + file_name + '.html"'
                return response
        raise Http404

    return action_error_check(after_check)


def get_module_list(request):
    def after_check():
        modules = Module.objects.all()
        data = ModulesBuilder(modules).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(result.get_data())

    return action_error_check(after_check)


def create_module(request):
    def after_check():
        request_json = get_post_request_json(request)
        serializer = ModuleSerializer(data=request_json)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    return action_permission_check(request, after_check)


# recovery - apply ruleset
def recover_rulesets(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_data = sync.sync_up_rulesets_from_backup(request_json, request.user)
        result = ResponseBuilder(data=result_data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


# ruleset log detail - apply ruleset
def apply_ruleset_to_server(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_data = sync.sync_up_ruleset_from_backup(request_json, request.user)
        result = ResponseBuilder(data=result_data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


# rulesets report job
def get_rulesets_report_job(request, scheduler_id):
    def after_check():
        scheduler_info = ReportSchedulerInfo.objects.get(id=scheduler_id)
        scheduler_data = ReportSchedulerInfoBuilder(request.user, scheduler_info).get_data()
        result = ResponseBuilder(data=scheduler_data).get_data()
        response = JsonResponse(data=result)
        return response

    return action_error_check(after_check)


def get_rulesets_report_jobs(request):
    def after_check():
        schedulers = report_scheduler.get_schedulers()
        data_list = list()
        for scheduler in schedulers:
            data_builder = ReportSchedulerInfoBuilder(request.user, scheduler)
            data_list.append(data_builder.get_data())
        result = ResponseBuilder(data=data_list).get_data()
        return JsonResponse(data=result)

    return action_error_check(after_check)


def create_ruleset_report_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        info_log("API", "create report job scheduler, request json =" + str(request_json))
        scheduler_info = report_scheduler.create_scheduler(request_json, request.user)
        info_data = ReportSchedulerInfoBuilder(request.user, scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def update_ruleset_report_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        info_log("API", "update report job scheduler, request json =" + str(request_json))
        scheduler_info = report_scheduler.update_report_scheduler(request_json, request.user)
        info_data = ReportSchedulerInfoBuilder(request.user, scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def update_rulesets_report_status(request):
    def after_check():
        request_json = get_post_request_json(request)
        scheduler = report_scheduler.update_scheduler_status(request_json, request.user)
        data = ReportSchedulerInfoBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def delete_ruleset_report_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        report_scheduler.delete_scheduler(request_json, request.user)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


# ruleset sync job
def get_rulesets_sync_jobs(request):
    def after_check():
        schedulers = sync_scheduler.get_schedulers()
        data_list = list()
        for scheduler in schedulers:
            data_builder = RulesetSyncSchedulerBuilder(scheduler)
            data_list.append(data_builder.get_data())

        result = ResponseBuilder(data=data_list).get_data()
        return JsonResponse(data=result)

    return action_error_check(after_check)


def run_rulesets_sync_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        parser = CreateRulesetSyncSchedulerParser(request_json, request.user)
        run_in_background(sync.sync_up_rulesets_without_scheduler, parser)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def create_rulesets_sync_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        scheduler = sync_scheduler.create_scheduler(request_json, request.user)
        data = RulesetSyncSchedulerBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def update_rulesets_sync_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        scheduler = sync_scheduler.update_scheduler(request_json, request.user)
        data = RulesetSyncSchedulerBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def update_rulesets_sync_job_status(request):
    def after_check():
        request_json = get_post_request_json(request)
        scheduler = sync_scheduler.update_scheduler_status(request_json, request.user)
        data = RulesetSyncSchedulerBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def delete_rulesets_sync_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        sync_scheduler.delete_scheduler(request_json, request.user)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def get_ruleset(request):
    def after_check():
        request_json = get_post_request_json(request)
        ruleset = log.get_ruleset(request_json)
        result = {KEY_RULESET_DATA: ruleset}
        return render(request, "ruleset_content_view.html", result)

    return action_error_check(after_check)


def create_ruleset(request):
    def after_check():
        sync.create_ruleset_test()

    return action_error_check(after_check)


def update_ruleset(request):
    def after_check():
        sync.update_ruleset_test()

    return action_error_check(after_check)
