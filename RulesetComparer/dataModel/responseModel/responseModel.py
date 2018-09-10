from RulesetComparer.resource import apiResponse as api
from django.http import JsonResponse
from abc import abstractmethod


class ResponseModel:
    def __init__(self):
        self.key_value_dict = {}
        self.error_code = None

    def set_error_code(self, error_code):
        self.error_code = error_code

    def get_response_json(self):
        # has define error
        if self.error_code is not None:
            self.key_value_dict[api.RESPONSE_KEY_STATUS_CODE] = self.error_code
            self.key_value_dict[api.RESPONSE_KEY_MESSAGE] = api.ERROR_MESSAGE_MAP[self.error_code]
        else:
            self.key_value_dict[api.RESPONSE_KEY_STATUS_CODE] = api.STATUS_CODE_SUCCESS
            self.key_value_dict[api.RESPONSE_KEY_MESSAGE] = api.MESSAGE_SUCCESS
            self.key_value_dict[api.RESPONSE_KEY_DATA] = self.get_content_json()

        return JsonResponse(self.key_value_dict)

    @abstractmethod
    def get_content_json(self):
        pass

