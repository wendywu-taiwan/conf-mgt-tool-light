from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *


class UserBuilder(BaseBuilder):
    def __init__(self, user):
        try:
            self.user = user
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        if self.user is None:
            return self.result_dict

        self.result_dict[KEY_ID] = self.user.id
        self.result_dict[KEY_NAME] = self.user.username
        self.result_dict[KEY_EMAIL] = self.user.email
