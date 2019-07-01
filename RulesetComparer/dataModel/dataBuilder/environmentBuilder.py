from RulesetComparer.dataModel.dataBuilder.baseBuilder import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment


class EnvironmentBuilder(BaseBuilder):
    ENVIRONMENT_BACKUP = "Backup"

    def __init__(self, environment_id):
        try:
            if environment_id is None:
                self.environment = None
            else:
                self.environment = Environment.objects.get(id=environment_id)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        if self.environment is None:
            self.result_dict[KEY_ID] = self.ENVIRONMENT_BACKUP
            self.result_dict[KEY_NAME] = self.ENVIRONMENT_BACKUP
            self.result_dict[KEY_FULL_NAME] = self.ENVIRONMENT_BACKUP
        else:
            self.result_dict[KEY_ID] = self.environment.id
            self.result_dict[KEY_NAME] = self.environment.name
            self.result_dict[KEY_FULL_NAME] = self.environment.full_name
