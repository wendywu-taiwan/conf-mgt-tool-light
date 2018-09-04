from RulesetComparer.responseModel.responseModel import ResponseModel
from RulesetComparer.resource import apiResponse


class DownloadRulesetModel(ResponseModel):
    ruleset_list = []

    def __init__(self, response_data, ruleset_list):
        ResponseModel.__init__(self, response_data)
        self.ruleset_list = ruleset_list

    def get_response_json(self):
        if self.response_data[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE] != 0:
            return ResponseModel.get_error_response_json(self, self.status_code(),
                                                         self.error_message())
        else:
            return ResponseModel.get_response_json(self, self.status_code(),
                                                   self.success_message())

    def get_content_json(self):
        return self.ruleset_list

    def status_code(self):
        return self.response_data[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE]

    def success_message(self):
        message_obj = self.response_data[apiResponse.B2B_RESPONSE_KEY_MESSAGE][0]
        message = message_obj[apiResponse.B2B_RESPONSE_KEY_MESSAGE_LOCALIZATION_TEXT]
        return message

    def error_message(self):
        message_obj = self.response_data[apiResponse.B2B_RESPONSE_KEY_MESSAGE][0]
        message_code = message_obj[apiResponse.B2B_RESPONSE_KEY_MESSAGE_CODE]
        text = message_obj[apiResponse.B2B_RESPONSE_KEY_MESSAGE_TEXT]
        return message_code + ', ' + text


