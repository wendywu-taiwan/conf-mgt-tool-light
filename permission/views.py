import traceback
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.utils import json

from RulesetComparer.date_model.json_builder.git_country_path_list import GitCountryPathListBuilder
from RulesetComparer.properties.key import *
from RulesetComparer.utils.logger import error_log
from common.data_object.json_builder.response import ResponseBuilder
from common.data_object.error.error import PermissionDeniedError
from common.data_object.error.message import PERMISSION_DENIED_MESSAGE
from common.data_object.error.status import PERMISSION_DENIED
from common.models import GitCountryPath
from common.services.git_manage_services import update_git_country_path
from common.views import page_permission_check, action_permission_check
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
        check_function_visibility(request, KEY_F_USER_ROLE, KEY_M_SETTING)
        data = {KEY_NAVIGATION_INFO: SettingInfoBuilder(request.user).get_data()}
        return render(request, "setting_base.html", data)

    return permission_check(request, after_check)


@login_required
def setting_user_role_list_page(request):
    def after_check():
        check_function_visibility(request, KEY_F_USER_ROLE, KEY_M_SETTING)
        data = get_user_role_list(request.user)
        return render(request, "user_role_list.html", data)

    return permission_check(request, after_check)


@login_required
def setting_user_role_edit_page(request, user_id):
    def after_check():
        check_function_visibility(request, KEY_F_USER_ROLE, KEY_M_SETTING)
        data = get_user_role_edit(request.user, user_id)
        return render(request, "user_role_edit.html", data)

    return permission_check(request, after_check)


@login_required
def edit_user_role(request):
    def after_check():
        check_function_visibility(request, KEY_F_USER_ROLE, KEY_M_SETTING)
        json_data = get_post_request_json(request)
        edit_user_role_data(json_data)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)

    return permission_check(request, after_check)


@login_required
def setting_role_permission_list_page(request):
    def after_check():
        check_function_visibility(request, KEY_F_ROLE_PERMISSION, KEY_M_SETTING)
        data = get_role_permission_list(request.user)
        return render(request, "role_permission_list.html", data)

    return permission_check(request, after_check)


@login_required
def setting_role_permission_edit_page(request, environment_id):
    def after_check():
        check_function_visibility(request, KEY_F_ROLE_PERMISSION, KEY_M_SETTING)
        data = get_role_permission_edit(request.user, environment_id)
        return render(request, "role_permission_edit.html", data)

    return permission_check(request, after_check)


@login_required
def edit_role_permission(request):
    def after_check():
        check_function_visibility(request, KEY_F_ROLE_PERMISSION, KEY_M_SETTING)
        json_data = get_post_request_json(request)
        edit_role_permission_data(json_data)
        result = ResponseBuilder().get_data()
        return JsonResponse(data=result)

    return permission_check(request, after_check)


@login_required
def admin_console_git_country_path_list_page(request):
    def check_visibility():
        pass
        check_function_visibility(request, KEY_F_GIT_PATH_MANGER, KEY_M_SETTING)

    def get_visible_data():
        return GitCountryPath.objects.filter(module__name=KEY_M_RULESET).values()

    def after_check(visible_data):
        check_function_visibility(request, KEY_F_GIT_PATH_MANGER, KEY_M_SETTING)
        data = GitCountryPathListBuilder(request.user, visible_data).get_data()
        return render(request, "git_country_path_list.html", data)

    return page_permission_check(request, check_visibility, get_visible_data, after_check)


@login_required
def admin_console_git_country_path_edit(request):
    def after_check():
        request_json = get_post_request_json(request)
        result_data = update_git_country_path(request_json)
        result = ResponseBuilder(data=result_data).get_data()
        return JsonResponse(data=result)

    return action_permission_check(request, after_check)


def get_post_request_json(request):
    if request.method != REQUEST_POST:
        return HttpResponseBadRequest
    else:
        try:
            request_json = json.loads(request.body.decode())
            return request_json
        except BaseException:
            error_log(traceback.format_exc())
