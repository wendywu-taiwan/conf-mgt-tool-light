from django.shortcuts import render, redirect
from django.http import JsonResponse

from common.data_object.error.status import NOT_SUPPORT_PREVIEW
from common.data_object.json_builder.response import ResponseBuilder
from common.utils.utility import get_post_request_json
from common.views import page_error_check
from shared_storage.properties.config import COMPARE_TYPE_BLACK_LIST
from shared_storage.services.services import *
from shared_storage.data_object.json_builder.bind_file_diff_result_builder import BindFolderFileDiffResultBuilder
from shared_storage.data_object.json_builder.bind_file_detail_builder import BindFileDetailBuilder, BindFileSameDetailBuilder


def select_to_compare_page(request):
    def after_check():
        if request.method == REQUEST_GET:
            regions = get_active_region_list()
            response = ResponseBuilder(data=regions).get_data()
            return render(request, "select_to_compare.html", response)
        elif request.method == REQUEST_POST:
            left_region_id = request.POST.get('left_region_id')
            left_environment_id = request.POST.get('left_environment_id')
            left_folder = request.POST.get('left_folder')
            right_region_id = request.POST.get('right_region_id')
            right_environment_id = request.POST.get('right_environment_id')
            right_folder = request.POST.get('right_folder')

            result_json = compare_shared_storage_folder(left_region_id, left_environment_id, left_folder,
                                                        right_region_id, right_environment_id, right_folder)
            response = ResponseBuilder(data=result_json).get_data()
            return render(request, "shared_storage_folder_compare_result.html", response)

    return page_error_check(after_check)


def select_to_compare_filter_environment_page(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = get_region_environment_list(request_json)
        return render(request, "select_to_compare_dropdown.html", result_json)

    return page_error_check(after_check)


def select_to_compare_filter_folder_page(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = get_environment_dir_list(request_json)
        return render(request, "select_to_compare_dropdown.html", result_json)

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
