from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.date_model.json_builder.admin_console_info import AdminConsoleInfoBuilder
from RulesetComparer.properties.key import KEY_NAVIGATION_INFO


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
        info_data = AdminConsoleInfoBuilder(self.user).get_data()
        self.result_dict[KEY_NAVIGATION_INFO] = info_data
        return self.result_dict
