from RulesetComparer.date_model.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer


class RecoverFilterObjBuilder(BaseBuilder):
    def __init__(self, country, environment, recover_backup_objects):
        try:
            self.recover_backup_objects = recover_backup_objects
            self.country = country
            self.environment = environment
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_COUNTRY] = CountrySerializer(self.country).data
        self.result_dict[KEY_ENVIRONMENT] = EnvironmentSerializer(self.environment).data
        self.result_dict[KEY_BACKUP_RULESETS_LIST] = self.__order_recover_backup_objects__()

    def __order_recover_backup_objects__(self):
        return sorted(self.recover_backup_objects, key=lambda k: k[KEY_FOLDER_NAME], reverse=True)
