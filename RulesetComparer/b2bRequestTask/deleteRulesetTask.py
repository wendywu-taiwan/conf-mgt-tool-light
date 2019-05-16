from RulesetComparer.b2bRequestTask.baseRequestTask import BaseRequestTask
from RulesetComparer.dataModel.xml.ruleSetFileListParser import RuleListModel
from RulesetComparer.properties import dataKey
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
