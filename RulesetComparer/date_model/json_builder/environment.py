from RulesetComparer.date_model.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment


class EnvironmentBuilder(BaseBuilder):

    def __init__(self, id=None, environment=None):
        try:
            if id is None:
                self.environment = environment
            else:
                self.environment = Environment.objects.get(id=id)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.environment.id
        self.result_dict[KEY_NAME] = self.environment.name
        self.result_dict[KEY_FULL_NAME] = self.environment.full_name


class EnvironmentsBuilder(BaseBuilder):

    def __init__(self, ids=None, environments=None):
        try:
            self.environments = []
            if ids is None:
                self.environments = environments
            else:
                for id in ids:
                    self.environments.append(Environment.objects.get(id=id))
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.parse_environments()

    def parse_environments(self):
        array = []
        for environment in self.environments:
            data = EnvironmentBuilder(environment=environment).get_data()
            array.append(data)
        return array
