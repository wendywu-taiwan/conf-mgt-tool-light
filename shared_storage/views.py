from django.shortcuts import render
from django.http import JsonResponse

from common.data_object.json_builder.response import ResponseBuilder
from common.views import page_error_check
from shared_storage.services.services import diff_country_level


def select_to_compare_page(request):
    def after_check():
        response = ResponseBuilder(data=None).get_data()
        return render(request, "select_to_compare.html", response)

    return page_error_check(after_check)
