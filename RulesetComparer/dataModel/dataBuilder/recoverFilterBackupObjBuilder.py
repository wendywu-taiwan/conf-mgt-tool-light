from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.utils.stringFilter import *


class RecoverFilterBackupObjBuilder(BaseBuilder):
    def __init__(self, ruleset_log_group, ruleset_logs):
        try:
            self.ruleset_log_group = ruleset_log_group
            self.ruleset_logs = ruleset_logs
            self.update_time = ruleset_log_group.update_time
            self.backup_key = ruleset_log_group.backup_key
            self.ruleset_count = len(ruleset_logs)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_UPDATE_TIME] = self.update_time
        self.result_dict[KEY_BACKUP_KEY] = self.backup_key
        self.result_dict[KEY_COUNT] = self.ruleset_count
        self.result_dict[KEY_RULESETS] = self.__generate_rulesets_object__()

    def __generate_rulesets_object__(self):
        rulesets_array = []

        for ruleset_log in self.ruleset_logs:
            ruleset_name = ruleset_log.get(KEY_RULESET_NAME)
            rulesets_array.append(ruleset_name)

        return rulesets_array
