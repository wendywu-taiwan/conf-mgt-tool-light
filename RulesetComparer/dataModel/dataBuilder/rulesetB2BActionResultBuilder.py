from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.dataKey import STATUS_SUCCESS, STATUS_FAILED


class RulesetB2BActionResultBuilder(BaseBuilder):
    def __init__(self, ruleset_name, action, b2b_response_data):
        try:
            self.action = action
            self.ruleset_name = ruleset_name
            self.b2b_response_data = b2b_response_data
            self.result_dict = {
                "ruleset_name": "",
                "action": "",
                "status": "",
                "exception": ""
            }
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict["ruleset_name"] = self.ruleset_name
        self.result_dict["action"] = self.action

        if self.b2b_response_data is None or self.b2b_response_data.returnCode != 0:
            b2b_message = self.b2b_response_data.message[0]
            self.result_dict["status"] = STATUS_FAILED
            self.result_dict["exception"] = b2b_message.localizedText
        else:
            self.result_dict["status"] = STATUS_SUCCESS
