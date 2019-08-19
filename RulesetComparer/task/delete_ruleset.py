from RulesetComparer.task.base_request import BaseRequestTask
from RulesetComparer.date_model.xml.ruleset_list import RuleListModel
from RulesetComparer.properties import key
from RulesetComparer.utils.logger import *


class DeleteRulesetTask(BaseRequestTask):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_COUNTRY = 'ownerId'
    LOG_CLASS = "DeleteRulesetTask"

    def execute(self):
        pass

    def parse_result_data(self):
        pass
