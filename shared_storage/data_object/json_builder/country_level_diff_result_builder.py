import traceback
from common.data_object.json_builder.base import BaseBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.ftp_region import FTPRegionBuilder
from RulesetComparer.properties.config import *


class CountryLevelDiffResultBuilder(BaseBuilder):
    def __init__(self, left_root_object, right_root_object, compare_key):
        try:
            self.left_root_object = left_root_object
            self.right_root_object = right_root_object
            self.compare_key = compare_key
            BaseBuilder.__init__(self)
        except Exception as e:
            traceback.print_exc()
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_LEFT_ENVIRONMENT] = EnvironmentBuilder(
            environment=self.left_root_object.environment).get_data()
        self.result_dict[KEY_RIGHT_ENVIRONMENT] = EnvironmentBuilder(
            environment=self.right_root_object.environment).get_data()
        self.result_dict[KEY_LEFT_REGION] = FTPRegionBuilder(id=self.left_root_object.region_id).get_data()
        self.result_dict[KEY_RIGHT_REGION] = FTPRegionBuilder(id=self.right_root_object.region_id).get_data()
        self.result_dict[KEY_LEFT_FOLDER] = self.left_root_object.folder
        self.result_dict[KEY_RIGHT_FOLDER] = self.right_root_object.folder
        self.result_dict[KEY_LEFT_DIFF_RESULT] = self.left_root_object.generate_compare_result_json()
        self.result_dict[KEY_RIGHT_DIFF_RESULT] = self.right_root_object.generate_compare_result_json()
        self.result_dict[KEY_COMPARE_HASH_KEY] = self.compare_key
