import traceback

from django.http import HttpRequest

from common.data_object.json_builder.base import BaseBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.ftp_region import FTPRegionBuilder
from RulesetComparer.properties.config import *


class SelectToDownloadFileListBuilder(BaseBuilder):
    def __init__(self, root_object):
        try:
            self.root_object = root_object
            self.result_list = self.root_object.generate_files_list_json()
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ENVIRONMENT] = EnvironmentBuilder(
            environment=self.root_object.environment).get_data()
        self.result_dict[KEY_REGION] = FTPRegionBuilder(id=self.root_object.region_id).get_data()
        self.result_dict[KEY_FOLDER] = self.root_object.folder
        self.result_dict[KEY_COMPARE_HASH_KEY] = self.root_object.dir_connect_obj.root_hash_key
        self.result_dict[KEY_DATA] = self.result_list
