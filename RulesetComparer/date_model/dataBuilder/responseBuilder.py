from RulesetComparer.date_model.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties import dataKey as key


class ResponseBuilder(BaseBuilder):
    def __init__(self, status_code=None, data=None, message=None):
        if status_code is None:
            self.status_code = 200
        else:
            self.status_code = status_code

        if data is None:
            self.data = ""
        else:
            self.data = data

        if message is None:
            self.message = key.SUCCESS_MESSAGE
        else:
            self.message = message
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict["data"] = self.data
        self.result_dict["message"] = self.message
        self.result_dict["status_code"] = self.status_code
