from django.shortcuts import render, redirect
from django.http import JsonResponse

from RulesetComparer.properties.key import KEY_PROPERTIES, REQUEST_GET, REQUEST_POST, KEY_DATA
from common.data_object.error.status import NOT_SUPPORT_PREVIEW, SUCCESS_NO_DATA
from common.data_object.json_builder.response import ResponseBuilder
from common.utils.utility import get_post_request_json
from common.views import page_error_check
from shared_storage.properties.config import COMPARE_TYPE_BLACK_LIST
from shared_storage.services import compare_services, download_services

from shared_storage.data_object.json_builder.bind_file_diff_result_builder import BindFolderFileDiffResultBuilder
from shared_storage.data_object.json_builder.bind_file_detail_builder import BindFileDetailBuilder, \
    BindFileSameDetailBuilder
from shared_storage.utils.file_manager import load_folder_file_diff_json
from shared_storage.services.download_services import filter_file_result, filter_second_folder


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
                                                                         right_environment_id, right_folder)
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
        if type in COMPARE_TYPE_BLACK_LIST:
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
        if file_type in COMPARE_TYPE_BLACK_LIST:
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


# def download_files(request):
#     def after_check():
#         if file_type in COMPARE_TYPE_BLACK_LIST:
#             result = ResponseBuilder(status_code=NOT_SUPPORT_PREVIEW).get_data()
#             return JsonResponse(result)
#
#         if diff_result == "same":
#             result_json = BindFileSameDetailBuilder(side, root_key, node_key).get_data()
#         else:
#             result_json = BindFileDetailBuilder(side, root_key, node_key).get_data()
#
#         response = ResponseBuilder(data=result_json).get_data()
#         return render(request, "shared_storage_file_detail.html", response)
#
#     return page_error_check(after_check)


def send_compare_result_mail(request):
    def after_check():
        left_region_id = 6
        left_environment_id = 6
        left_folder = "kr"
        right_region_id = 8
        right_environment_id = 7
        right_folder = "kr"
        result_json = compare_services.compare_shared_storage_folder_mail_result(request, left_region_id,
                                                                                 left_environment_id,
                                                                                 left_folder, right_region_id,
                                                                                 right_environment_id,
                                                                                 right_folder)
        compare_services.send_shared_storage_compare_result_mail(result_json)

    return page_error_check(after_check)
