from abc import abstractmethod

from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.date_model.json_builder.admin_console_info import AdminConsoleInfoBuilder as rulesetBuilder
from RulesetComparer.properties.key import KEY_NAVIGATION_INFO
from shared_storage.data_object.json_builder.admin_console_info_builder import \
    AdminConsoleInfoBuilder as sharedStorageBuilder


class AdminConsoleBaseBuilder(BaseBuilder):

    def __init__(self, user):
        try:
            self.user = user
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    @staticmethod
    def get_current_time():
        return super().get_current_time

    def __generate_data__(self):
        pass

    def get_data(self):
        if self.user is None:
            return self.result_dict

        self.result_dict = super().get_data()
        self.result_dict[KEY_NAVIGATION_INFO] = self.get_info_data()
        return self.result_dict

    @abstractmethod
    def get_info_data(self):
        pass


class AdminConsoleRulesetBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user):
        AdminConsoleBaseBuilder.__init__(self, user)

    def get_info_data(self):
        return rulesetBuilder(self.user).get_data()


class AdminConsoleSharedStorageBuilder(AdminConsoleBaseBuilder):

    def __init__(self, user):
        AdminConsoleBaseBuilder.__init__(self, user)

    def get_info_data(self):
        return sharedStorageBuilder(self.user).get_data()
