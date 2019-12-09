import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404

from shared_storage.data_object.json_builder.report_scheduler_create_page import ReportSchedulerCreatePageBuilder
from shared_storage.data_object.json_builder.shared_storage_report_scheduler import SharedStorageSchedulersBuilder, \
    SharedStorageReportSchedulerBuilder
from shared_storage.data_object.json_builder.report_scheduler_update_page import ReportSchedulerUpdatePageBuilder
from RulesetComparer.properties.key import *
from RulesetComparer.utils.logger import info_log
from common.data_object.error.status import NOT_SUPPORT_PREVIEW, SUCCESS_NO_DATA
from common.data_object.json_builder.response import ResponseBuilder
from common.utils.utility import get_post_request_json
from common.views import page_error_check, action_error_check, page_permission_check, action_permission_check
from permission.utils.permission_manager import check_function_visibility
from shared_storage.data_object.json_builder.admin_console_info_builder import AdminConsoleInfoBuilder
from shared_storage.properties.config import COMPARE_TYPE_WHITE_LIST
from shared_storage.services import compare_services, download_services

from shared_storage.data_object.json_builder.bind_file_diff_result_builder import BindFolderFileDiffResultBuilder
from shared_storage.data_object.json_builder.bind_file_detail_builder import BindFileDetailBuilder, \
    BindFileSameDetailBuilder
from shared_storage.utils.file_manager import load_folder_file_diff_json
from shared_storage.models import SharedStorageReportScheduler
from shared_storage.services import report_scheduler_services


# backend page
@login_required
def admin_console_page(request):
    data = {KEY_NAVIGATION_INFO: AdminConsoleInfoBuilder(request.user).get_data()}
    return render(request, "shared_storage_admin_console_base.html", data)


@login_required
def admin_console_report_scheduler_list_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_REPORT_TASK, KEY_M_SHARED_STORAGE)

    def get_visible_data():
        return SharedStorageReportScheduler.objects.get_visible_schedulers(request.user.id)

    def after_check(visible_data):
        data = SharedStorageSchedulersBuilder(request.user, visible_data).get_data()
        return render(request, "shared_storage_report_scheduler_list.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_report_scheduler_create_page(request):
    def check_visibility():
        check_function_visibility(request, KEY_F_REPORT_TASK, KEY_M_SHARED_STORAGE)

    def get_visible_data():
        regions = compare_services.get_active_region_list()
        return regions

    def after_check(visible_data):
        data = ReportSchedulerCreatePageBuilder(request.user, visible_data).get_data()
        return render(request, "shared_storage_report_scheduler_create.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_report_scheduler_update_page(request, scheduler_id):
    def check_visibility():
        check_function_visibility(request, KEY_F_REPORT_TASK, KEY_M_SHARED_STORAGE)

    def get_visible_data():
        regions = compare_services.get_active_region_list()
        return regions

    def after_check(visible_data):
        data = ReportSchedulerUpdatePageBuilder(request.user, visible_data, scheduler_id).get_data()
        return render(request, "shared_storage_report_scheduler_update.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


# frontend page
def select_to_compare_page(request):
    def after_check():
        if request.method == REQUEST_GET:
            regions = compare_services.get_active_region_list()
            response = ResponseBuilder(data=regions).get_data()
            return render(request, "select_to_compare.html", response)
        elif request.method == REQUEST_POST:
            left_region_id = request.POST.get('left_region_id')
            left_environment_id = request.POST.get('left_environment_id')
            left_folder = request.POST.get('left_folder')
            right_region_id = request.POST.get('right_region_id')
            right_environment_id = request.POST.get('right_environment_id')
            right_folder = request.POST.get('right_folder')
            #
            result_json = compare_services.compare_shared_storage_folder(left_region_id, left_environment_id,
                                                                         left_folder, right_region_id,
                                                                         right_environment_id, right_folder, False)
            #
            response = ResponseBuilder(data=result_json).get_data()
            return render(request, "shared_storage_folder_compare_result.html", response)

    return page_error_check(after_check)


def select_to_compare_filter_environment(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = compare_services.get_region_environment_list(request_json)
        return render(request, "select_to_compare_dropdown.html", result_json)

    return page_error_check(after_check)


def select_to_compare_filter_folder(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = compare_services.get_environment_dir_list(request_json)
        return render(request, "select_to_compare_dropdown.html", result_json)

    return page_error_check(after_check)


def select_to_compare_result_page(request, root_key):
    def after_check():
        result_json = load_folder_file_diff_json(root_key)
        response = ResponseBuilder(data=result_json).get_data()
        return render(request, "shared_storage_folder_compare_result.html", response)

    return page_error_check(after_check)


def select_to_compare_file_diff_page(request, root_key, node_key, type):
    def after_check():
        if type not in COMPARE_TYPE_WHITE_LIST:
            result = ResponseBuilder(status_code=NOT_SUPPORT_PREVIEW).get_data()
            return JsonResponse(result)
        else:
            result_json = BindFolderFileDiffResultBuilder(root_key, node_key).get_data()
            if type == KEY_PROPERTIES:
                response = ResponseBuilder(data=result_json).get_data()
                return render(request, "shared_storage_properties_file_diff.html", response)
            else:
                response = ResponseBuilder(data=result_json).get_data()
                return render(request, "shared_storage_string_file_diff.html", response)

    return page_error_check(after_check)


def select_to_compare_file_detail_page(request, side, root_key, node_key, diff_result, file_type):
    def after_check():
        if file_type not in COMPARE_TYPE_WHITE_LIST:
            result = ResponseBuilder(status_code=NOT_SUPPORT_PREVIEW).get_data()
            return JsonResponse(result)

        if diff_result == "same":
            result_json = BindFileSameDetailBuilder(side, root_key, node_key).get_data()
        else:
            result_json = BindFileDetailBuilder(side, root_key, node_key).get_data()

        response = ResponseBuilder(data=result_json).get_data()
        return render(request, "shared_storage_file_detail.html", response)

    return page_error_check(after_check)


def select_to_download_page(request):
    def after_check():
        regions = compare_services.get_active_region_list()
        response = ResponseBuilder(data=regions).get_data()
        return render(request, "select_to_download.html", response)

    return page_error_check(after_check)


def select_to_download_filter_environment(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = download_services.get_region_environment_list(request_json)
        return render(request, "dropdown_component.html", result_json)

    return page_error_check(after_check)


def select_to_download_filter_folder(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = download_services.get_environment_dir_list(request_json)
        return render(request, "dropdown_component.html", result_json)

    return page_error_check(after_check)


def select_to_download_filter_module_folder(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = download_services.filter_second_folder(request_json)
        return render(request, "dropdown_component.html", result_json)

    return page_error_check(after_check)


def select_to_download_filter_latest_version_folder(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = download_services.filter_latest_version_folder(request_json)
        return render(request, "dropdown_component.html", result_json)

    return page_error_check(after_check)


def select_to_download_filter_result_page(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = download_services.filter_file_result(request_json)
        result_data_list = result_json.get(KEY_DATA)
        if len(result_data_list) == 0:
            result = ResponseBuilder(status_code=SUCCESS_NO_DATA).get_data()
            return JsonResponse(result)
        else:
            return render(request, "download_filter_result.html", result_json)

    return page_error_check(after_check)


def select_to_download_file_list_page(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = download_services.file_list(request_json)
        return render(request, "download_file_list.html", result_json)

    return page_error_check(after_check)


def download_files(request):
    def after_check():
        request_json = get_post_request_json(request)
        zip_file_path = download_services.download_files(request_json)

        if os.path.exists(zip_file_path):
            with open(zip_file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                return response
        raise Http404

    return action_error_check(after_check)


def download_exist_files(request):
    def after_check():
        request_json = get_post_request_json(request)
        zip_file_path = download_services.download_exist_files(request_json)

        if os.path.exists(zip_file_path):
            with open(zip_file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/zip")
                return response
        raise Http404

    return action_error_check(after_check)


def send_compare_result_mail(request):
    def after_check():
        left_region_id = 6
        left_environment_id = 6
        left_folder = "kr"
        right_region_id = 8
        right_environment_id = 7
        right_folder = "kr"
        result_json = compare_services.compare_shared_storage_folder(left_region_id, left_environment_id, left_folder,
                                                                     right_region_id, right_environment_id,
                                                                     right_folder,
                                                                     True, request.get_host())
        compare_services.send_shared_storage_compare_result_mail(result_json)

    return page_error_check(after_check)


def create_report_scheduler_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        info_log(KEY_M_SHARED_STORAGE, "create report scheduler, request json =" + str(request_json))
        scheduler_info = report_scheduler_services.create_scheduler(request_json, request.user, request.get_host())
        info_data = SharedStorageReportSchedulerBuilder(request.user, scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def update_report_scheduler_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        info_log(KEY_M_SHARED_STORAGE, "update report scheduler, request json =" + str(request_json))
        scheduler_info = report_scheduler_services.update_scheduler(request_json, request.user, request.get_host())
        info_data = SharedStorageReportSchedulerBuilder(request.user, scheduler_info).get_data()
        result = ResponseBuilder(data=info_data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def update_report_scheduler_status(request):
    def after_check():
        request_json = get_post_request_json(request)
        scheduler = report_scheduler_services.update_scheduler_status(request_json, request.user)
        data = SharedStorageReportSchedulerBuilder(request.user, scheduler).get_data()
        result = ResponseBuilder(data=data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def delete_report_scheduler_job(request):
    def after_check():
        request_json = get_post_request_json(request)
        report_scheduler_services.delete_scheduler(request_json, request.user)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)
