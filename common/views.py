import traceback

from django.shortcuts import render
from django.http import JsonResponse
from RulesetComparer.utils.logger import error_log
from common.data_object.error.error import PermissionDeniedError, B2BRulesetNotFoundError, \
    SharedStorageFolderNotFoundError, SharedStorageFTPServerConnectFailError, NoAvailableDataError
from common.data_object.error.message import PERMISSION_DENIED_MESSAGE, RULESET_NOT_FOUND_MESSAGE, \
    FOLDER_NOT_EXIST_MESSAGE, CONNECT_TO_FTP_SERVER_FAIL_MESSAGE, NO_AVAILABLE_DATA_MESSAGE
from common.data_object.error.status import RULESET_NOT_FOUND, PERMISSION_DENIED, FOLDER_NOT_EXIST, \
    CANT_CONNECT_FTP_SERVER, NO_AVAILABLE_DATA
from common.data_object.json_builder.response import ResponseBuilder


def page_permission_check(request, check_visibility, get_visible_data, executor):
    try:
        check_visibility()
        return executor(get_visible_data())
    except NoAvailableDataError:
        data = ResponseBuilder(status_code=NO_AVAILABLE_DATA, message=NO_AVAILABLE_DATA_MESSAGE).get_data()
        return JsonResponse(data)
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
    except SharedStorageFTPServerConnectFailError:
        result = ResponseBuilder(status_code=CANT_CONNECT_FTP_SERVER,
                                 message=CONNECT_TO_FTP_SERVER_FAIL_MESSAGE).get_data()
        return JsonResponse(result)
    except SharedStorageFolderNotFoundError:
        result = ResponseBuilder(status_code=FOLDER_NOT_EXIST, message=FOLDER_NOT_EXIST_MESSAGE).get_data()
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
        return JsonResponse(data)
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
