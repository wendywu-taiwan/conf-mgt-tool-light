import traceback

from django.http import HttpRequest

from common.data_object.json_builder.base import BaseBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.ftp_region import FTPRegionBuilder
from RulesetComparer.properties.config import *


class CountryLevelDiffMailResultBuilder(BaseBuilder):
    def __init__(self, left_root_object, right_root_object, compare_key):
        try:
            self.left_root_object = left_root_object
            self.right_root_object = right_root_object
            self.compare_key = compare_key
            self.left_only_list = list()
            self.right_only_list = list()
            self.different_list = list()
            self.left_root_object.generate_mail_json(self.left_only_list, self.right_only_list, self.different_list)
            self.has_changes = self.check_has_changes()
            BaseBuilder.__init__(self)
        except Exception as e:
            traceback.print_exc()
            raise e

    def check_has_changes(self):
        if len(self.right_only_list) > 0 or len(self.left_only_list) > 0 or len(self.different_list) > 0:
            return True
        else:
            return False

    def __generate_data__(self):
        self.result_dict[KEY_LEFT_ENVIRONMENT] = EnvironmentBuilder(
            environment=self.left_root_object.environment).get_data()
        self.result_dict[KEY_RIGHT_ENVIRONMENT] = EnvironmentBuilder(
            environment=self.right_root_object.environment).get_data()
        self.result_dict[KEY_LEFT_REGION] = FTPRegionBuilder(id=self.left_root_object.region_id).get_data()
        self.result_dict[KEY_RIGHT_REGION] = FTPRegionBuilder(id=self.right_root_object.region_id).get_data()
        self.result_dict[KEY_LEFT_FOLDER] = self.left_root_object.folder
        self.result_dict[KEY_RIGHT_FOLDER] = self.right_root_object.folder
        self.result_dict[KEY_COMPARE_HASH_KEY] = self.compare_key
        self.result_dict[KEY_LEFT_ONLY_DATA] = self.left_only_list
        self.result_dict[KEY_RIGHT_ONLY_DATA] = self.right_only_list
        self.result_dict[KEY_DIFFERENT] = self.different_list
        self.result_dict[KEY_HAS_CHANGES] = self.has_changes
