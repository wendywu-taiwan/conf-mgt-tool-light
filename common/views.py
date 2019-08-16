import traceback

from django.shortcuts import render
from django.http import JsonResponse
from RulesetComparer.date_model.json_builder.response import ResponseBuilder
from RulesetComparer.properties.message import PERMISSION_DENIED_MESSAGE
from RulesetComparer.properties.status_code import PERMISSION_DENIED
from RulesetComparer.utils.logger import error_log
from common.data_object.error.PermissionDeniedError import PermissionDeniedError


# Create your views here.

def page_permission_check(request, check_visibility, get_visible_data, executor):
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


def page_error_check(executor):
    try:
        return executor()
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def action_permission_check(request, executor):
    try:
        return executor()
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


def action_error_check(executor):
    try:
        return executor()
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)