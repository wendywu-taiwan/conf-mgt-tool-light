import json
from RulesetComparer.resource import apiResponse as api
from django.http import JsonResponse
from abc import abstractmethod


class ResponseModel:

    def __init__(self, response_data=None, error_code=None):
        self.key_value_dict = {}
        self.response_data = response_data
        self.error_code = error_code

    def set_error_code(self, error_code):
        self.error_code = error_code

    def get_response_json(self):
        # has define error
        if self.error_code is not None:
            self.key_value_dict[api.RESPONSE_KEY_STATUS_CODE] = self.error_code
            self.key_value_dict[api.RESPONSE_KEY_MESSAGE] = api.ERROR_MESSAGE_MAP[self.error_code]
        # empty response
        elif self.response_data is None:
            self.key_value_dict[api.RESPONSE_KEY_STATUS_CODE] = api.STATUS_CODE_NO_RESPONSE
            self.key_value_dict[api.RESPONSE_KEY_MESSAGE] = api.MESSAGE_NO_RESPONSE
        # request get failure result
        elif self.request_fail() is True:
            self.key_value_dict[api.RESPONSE_KEY_STATUS_CODE] = self.status_code()
            self.key_value_dict[api.RESPONSE_KEY_MESSAGE] = self.error_message()
        # request get success result
        else:
            self.key_value_dict[api.RESPONSE_KEY_STATUS_CODE] = self.status_code()
            self.key_value_dict[api.RESPONSE_KEY_MESSAGE] = self.success_message()
            self.key_value_dict[api.RESPONSE_KEY_DATA] = self.get_content_json()

        return JsonResponse(self.key_value_dict)

    @abstractmethod
    def get_content_json(self):
        pass

    @abstractmethod
    def status_code(self):
        pass

    @abstractmethod
    def request_fail(self):
        pass

    @abstractmethod
    def success_message(self):
        pass

    @abstractmethod
    def error_message(self):
        pass

