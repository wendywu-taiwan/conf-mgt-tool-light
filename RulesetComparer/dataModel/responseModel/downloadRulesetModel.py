from RulesetComparer.dataModel.responseModel.b2bResponseModel import ResponseModel
from RulesetComparer.resource import apiResponse


class DownloadRulesetModel(ResponseModel):

    def __init__(self, response_data=None, ruleset_list=None):
        ResponseModel.__init__(self, response_data)
        self.ruleset_list = ruleset_list
        if self.ruleset_list is None:
            self.ruleset_list = []

    def get_content_json(self):
        return self.ruleset_list

    def status_code(self):
        return self.response_data[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE]

    def request_fail(self):
        if self.status_code() == 0:
            return False
        else:
            return True

    def success_message(self):
        message_obj = self.response_data[apiResponse.B2B_RESPONSE_KEY_MESSAGE][0]
        message = message_obj[apiResponse.B2B_RESPONSE_KEY_MESSAGE_LOCALIZATION_TEXT]
        return message

    def error_message(self):
        message_obj = self.response_data[apiResponse.B2B_RESPONSE_KEY_MESSAGE][0]
        message_code = message_obj[apiResponse.B2B_RESPONSE_KEY_MESSAGE_CODE]
        text = message_obj[apiResponse.B2B_RESPONSE_KEY_MESSAGE_TEXT]
        return message_code + ', ' + text


