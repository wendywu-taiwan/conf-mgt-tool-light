from django.http import JsonResponse

from common.data_object.json_builder.response import ResponseBuilder
from common.views import page_error_check
from shared_storage.services.services import diff_country_level


def shared_storage_diff_page(request):
    def after_check():
        diff_country_level()
        result = ResponseBuilder(data=None).get_data()
        return JsonResponse(result.get_data())

    return page_error_check(after_check)
