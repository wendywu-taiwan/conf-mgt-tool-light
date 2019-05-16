from abc import abstractmethod
from RulesetComparer.utils import timeUtil
from RulesetComparer.properties import config


class BaseBuilder:
    def __init__(self):
        self.result_dict = {}
        self.__generate_data__()

    @staticmethod
    def get_current_time():
        return timeUtil.get_format_current_time(config.TIME_FORMAT.get("year_month_date"))

    @abstractmethod
    def __generate_data__(self):
        pass

    def get_data(self):
        return self.result_dict

