import json
from RulesetComparer.resource import apiResponse
from django.http import JsonResponse
from abc import abstractmethod

KEY_STATUS_CODE = 'api_ret_code'
KEY_MESSAGE = 'api_ret_message'
KEY_DATA = 'data'


class ResponseModel:

    def __init__(self, response_data):
        self.key_value_dict = {}
        self.response_data = response_data

    def get_error_response_json(self, status_code, message):
        self.key_value_dict[KEY_STATUS_CODE] = status_code
        self.key_value_dict[KEY_MESSAGE] = message
        return JsonResponse(self.key_value_dict)

    def get_response_json(self, status_code, message):
        if self.response_data is None:
            return self.get_error_response_json(self,
                                                apiResponse.STATUS_CODE_NO_RESPONSE,
                                                apiResponse.MESSAGE_NO_RESPONSE)

        self.key_value_dict[KEY_STATUS_CODE] = status_code
        self.key_value_dict[KEY_MESSAGE] = message
        self.key_value_dict[KEY_DATA] = self.get_content_json()
        return JsonResponse(self.key_value_dict)

    @abstractmethod
    def get_content_json(self):
        pass

