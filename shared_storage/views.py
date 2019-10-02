from django.shortcuts import render
from django.http import JsonResponse

from common.data_object.json_builder.response import ResponseBuilder
from common.utils.utility import get_post_request_json
from common.views import page_error_check
from shared_storage.services.services import *


def select_to_compare_page(request):
    def after_check():
        regions = get_active_region_list()
        response = ResponseBuilder(data=regions).get_data()
        return render(request, "select_to_compare.html", response)

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


def compare_shared_storage_folder_result_page(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_json = compare_shared_storage_folder(request_json)
        response = ResponseBuilder(data=result_json).get_data()
        return render(request, "shared_storage_folder_compare_result.html", response)

    return page_error_check(after_check)
