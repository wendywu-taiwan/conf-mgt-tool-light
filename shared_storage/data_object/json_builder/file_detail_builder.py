from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.config import *


class FileDetailBuilder(BaseBuilder):
    def __init__(self, file_object):
        try:
            self.file_object = file_object
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_FILE_NAME] = self.file_object.file_name
        self.result_dict[KEY_FILE_PATH] = self.file_object.file_path
        self.result_dict[KEY_FILE_SIZE] = self.file_object.file_size
        self.result_dict[KEY_MODIFICATION_TIME] = self.file_object.modification_time
