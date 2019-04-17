from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *


class RecoverFilterObjBuilder(BaseBuilder):
    def __init__(self, pre_json, recover_backup_objects):
        try:
            self.recover_backup_objects = recover_backup_objects
            self.json_data = pre_json
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_COUNTRY] = self.json_data.get(KEY_COUNTRY)
        self.result_dict[KEY_ENVIRONMENT] = self.json_data.get(KEY_TARGET_ENV)
        self.result_dict[KEY_BACKUP_RULESETS_LIST] = self.recover_backup_objects
