from RulesetComparer.responseModel.downloadRulesetModel import DownloadRulesetModel

from RulesetComparer.resource import apiResponse


class DownloadSingleRulesetModel(DownloadRulesetModel):

    def __init__(self, response_data, ruleset_name):
        DownloadRulesetModel.__init__(self, response_data)
        self.response_data = response_data
        self.ruleset_name = ruleset_name

        if self.request_fail() is False:
            self.status = 'success'
        else:
            self.status = 'fail'

    def get_content_json(self):
        return {apiResponse.DATA_KEY_RULESET_NAME: self.ruleset_name,
                apiResponse.DATA_KEY_DOWNLOAD_STATUS: self.status}

