import json
from RulesetComparer.properties import apiResponse as api
from django.http import JsonResponse
from abc import abstractmethod


class BaseRequestTask:

    def __init__(self, error_code=None):
        self.request_key_value = {}
        self.b2b_response_data = None
        self.response_data = {}
        self.error_code = error_code
        self.request_data()

    # request
    def request_parameter(self):
        parameter = []
        if len(self.request_key_value) == 0:
            return parameter

        for key, value in self.request_key_value.items():
            parameter.append(self.compose_key_value(key, value))

        return parameter

    def add_request_parameter(self, key, value):
        self.request_key_value[key] = value

    @staticmethod
    def compose_key_value(key, value):
        return {'name': key, 'value': value}

    # b2b response
    def status_code(self):
        return self.b2b_response_data[api.B2B_RESPONSE_KEY_RETURN_CODE]

    def b2b_response_error_check(self):
        if self.error_code is not None:
            return

        if self.b2b_response_data is None:
            self.error_code = api.STATUS_CODE_NO_RESPONSE

        if self.status_code() != 0:
            self.error_code = self.status_code()

    def success_message(self):
        message_obj = self.b2b_response_data[api.B2B_RESPONSE_KEY_MESSAGE][0]
        message = message_obj[api.B2B_RESPONSE_KEY_MESSAGE_LOCALIZATION_TEXT]
        return message

    def error_message(self):
        message_obj = self.b2b_response_data[api.B2B_RESPONSE_KEY_MESSAGE][0]
        message_code = message_obj[api.B2B_RESPONSE_KEY_MESSAGE_CODE]
        text = message_obj[api.B2B_RESPONSE_KEY_MESSAGE_TEXT]
        return message_code + ', ' + text

    # response
    def get_response_data(self):
        # success request
        if self.error_code is None:
            self.response_data[api.RESPONSE_KEY_STATUS_CODE] = self.status_code()
            self.response_data[api.RESPONSE_KEY_MESSAGE] = self.success_message()
            self.response_data[api.RESPONSE_KEY_DATA] = self.get_content_json()
        # failure response from b2b service
        elif self.error_code == self.status_code():
            self.response_data[api.RESPONSE_KEY_STATUS_CODE] = self.status_code()
            self.response_data[api.RESPONSE_KEY_MESSAGE] = self.error_message()
        # other failure
        else:
            self.response_data[api.RESPONSE_KEY_STATUS_CODE] = self.error_code
            self.response_data[api.RESPONSE_KEY_MESSAGE] = api.ERROR_MESSAGE_MAP[self.error_code]

        return self.response_data

    def get_response_json(self):
        return JsonResponse(self.get_response_data())

    def request_fail(self):
        if self.error_code is not None:
            return True
        else:
            return False

    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def get_content_json(self):
        pass

    @abstractmethod
    def request_data(self):
        pass
