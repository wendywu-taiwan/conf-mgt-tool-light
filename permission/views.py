import traceback
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.utils import json
from RulesetComparer.date_model.json_builder.response import ResponseBuilder
from RulesetComparer.properties.key import *
from RulesetComparer.properties.message import PERMISSION_DENIED_MESSAGE
from RulesetComparer.properties.status_code import PERMISSION_DENIED
from RulesetComparer.utils.logger import error_log
from common.data_object.error.PermissionDeniedError import PermissionDeniedError
from permission.utils.permission_manager import check_function_visibility
from permission.services.user_role import get_user_role_list, get_user_role_edit, edit_user_role_data
from permission.data_object.json_builder.setting_info import SettingInfoBuilder
from permission.services.role_permission import *


def permission_check(request, executor):
    try:
        return executor()
    except PermissionDeniedError:
        data = ResponseBuilder(status_code=PERMISSION_DENIED, message=PERMISSION_DENIED_MESSAGE).get_data()
        return render(request, "permission_denied.html", data)
    except Exception:
        error_log(traceback.format_exc())
        result = ResponseBuilder(status_code=500, message="Internal Server Error").get_data()
        return JsonResponse(result)


@login_required
def permission_index_page(request):
    def after_check():
        check_function_visibility(request, KEY_F_USER_ROLE)
        data = {KEY_NAVIGATION_INFO: SettingInfoBuilder(request.user).get_data()}
        return render(request, "setting_base.html", data)

    return permission_check(request, after_check)


@login_required
def setting_user_role_list_page(request):
    def after_check():
        check_function_visibility(request, KEY_F_USER_ROLE)
        data = get_user_role_list(request.user)
        return render(request, "user_role_list.html", data)

    return permission_check(request, after_check)


@login_required
def setting_user_role_edit_page(request, user_id):
    def after_check():
        check_function_visibility(request, KEY_F_USER_ROLE)
        data = get_user_role_edit(request.user, user_id)
        return render(request, "user_role_edit.html", data)

    return permission_check(request, after_check)


@login_required
def edit_user_role(request):
    def after_check():
        check_function_visibility(request, KEY_F_USER_ROLE)
        json_data = get_post_request_json(request)
        edit_user_role_data(json_data)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)

    return permission_check(request, after_check)


@login_required
def setting_role_permission_list_page(request):
    def after_check():
        check_function_visibility(request, KEY_F_ROLE_PERMISSION)
        data = get_role_permission_list(request.user)
        return render(request, "role_permission_list.html", data)

    return permission_check(request, after_check)


@login_required
def setting_role_permission_edit_page(request, environment_id):
    def after_check():
        check_function_visibility(request, KEY_F_ROLE_PERMISSION)
        data = get_role_permission_edit(request.user, environment_id)
        return render(request, "role_permission_edit.html", data)

    return permission_check(request, after_check)


def get_post_request_json(request):
    if request.method != REQUEST_POST:
        return HttpResponseBadRequest
    else:
        try:
            request_json = json.loads(request.body.decode())
            return request_json
        except BaseException:
            error_log(traceback.format_exc())
