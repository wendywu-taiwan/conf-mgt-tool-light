from abc import abstractmethod


class BaseBuilder:
    def __init__(self):
        self.result_dict = {}
        self.__generate_data__()

    @abstractmethod
    def __generate_data__(self):
        pass

    def get_data(self):
        return self.result_dict

