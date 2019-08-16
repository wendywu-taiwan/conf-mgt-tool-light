import traceback

from django.shortcuts import render
from django.http import JsonResponse
from RulesetComparer.utils.logger import error_log
from common.data_object.error.error import PermissionDeniedError, B2BRulesetNotFoundError
from common.data_object.error.message import PERMISSION_DENIED_MESSAGE, RULESET_NOT_FOUND_MESSAGE
from common.data_object.error.status import RULESET_NOT_FOUND, PERMISSION_DENIED
from common.data_object.json_builder.response import ResponseBuilder


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
    except B2BRulesetNotFoundError:
        result = ResponseBuilder(status_code=RULESET_NOT_FOUND, message=RULESET_NOT_FOUND_MESSAGE).get_data()
        return JsonResponse(result)
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
    except B2BRulesetNotFoundError:
        result = ResponseBuilder(status_code=RULESET_NOT_FOUND, message=RULESET_NOT_FOUND_MESSAGE).get_data()
        return JsonResponse(result)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)
