import traceback

from django.http import HttpResponseBadRequest
from rest_framework.utils import json

from RulesetComparer.properties.key import REQUEST_POST
from RulesetComparer.utils.logger import error_log


def string_builder(str_list):
    return "".join(str_list)


def get_union(list_a, list_b):
    return [i for i in list_a if i in list_b]


def to_int_list(my_list):
    return [int(i) for i in my_list]


def contains(my_list, text):
    if str(text) in str(my_list):
        return True
    else:
        return False


def get_post_request_json(request):
    if request.method != REQUEST_POST:
        return HttpResponseBadRequest
    else:
        try:
            request_json = json.loads(request.body.decode())
            return request_json
        except BaseException:
            error_log(traceback.format_exc())
