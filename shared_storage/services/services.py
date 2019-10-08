import traceback
import json
from permission.models import Environment
from shared_storage.data_object.dir_root_object import DirRootObject
from shared_storage.data_object.dir_node_diff_object import DirNodeDiffObject, DirNodeDiffFilterObject
from shared_storage.properties.config import COMPARE_RESULT_PATH
from shared_storage.data_object.json_builder.country_level_diff_result_builder import CountryLevelDiffResultBuilder
from common.data_object.ftp_connect_object import SharedStorageConnectionObject
from common.data_object.git_connect_object import SharedStorageGitConnectObject
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.fileManager import save_file, load_json_file
from permission.models import FTPRegion, FTPServer
from common.data_object.json_builder.environment import EnvironmentsBuilder
from common.data_object.json_builder.ftp_region import FTPRegionsBuilder
from shared_storage.data_object.json_builder.select_to_compare_filter_environment import \
    SelectToCompareFilterEnvironmentBuilder
from shared_storage.data_object.json_parser.select_to_compare_filter_environment import \
    SelectToCompareFilterEnvironmentParser
from shared_storage.data_object.json_builder.select_to_compare_filter_folder import \
    SelectToCompareFilterFolderBuilder
from shared_storage.data_object.json_parser.select_to_compare_filter_folder import \
    SelectToCompareFilterEnvironmentParser
from shared_storage.data_object.json_parser.compare_shared_storage_folder import CompareSharedStorageFolderParser


def get_active_region_list():
    try:
        region_id_list = FTPRegion.objects.filter(active=1).values_list("id", flat=True)
        data = FTPRegionsBuilder(ids=region_id_list).get_data()
        return data
    except Exception as e:
        raise e


def get_region_environment_list(json_data):
    try:
        parser = SelectToCompareFilterEnvironmentParser(json_data)
        environment_list = FTPServer.objects.filter(region__id=parser.region_id).values_list("environment_id",
                                                                                             flat=True)
        environments_json = EnvironmentsBuilder(ids=environment_list).get_data()
        result_json = SelectToCompareFilterEnvironmentBuilder(parser.side, environments_json).get_data()
        return result_json
    except Exception as e:
        raise e


def get_environment_dir_list(json_data):
    try:
        parser = SelectToCompareFilterEnvironmentParser(json_data)
        environment = Environment.objects.get(id=parser.environment_id)
        if environment.name == GIT_NAME:
            dir_connect_obj = SharedStorageGitConnectObject(False)
        else:
            dir_connect_obj = SharedStorageConnectionObject(parser.region_id, parser.environment_id, False)

        list_dir = dir_connect_obj.get_path_list_dir("")
        result_json = SelectToCompareFilterFolderBuilder(parser.side, list_dir).get_data()
        return result_json
    except Exception as e:
        raise e


def compare_shared_storage_folder(left_region_id, left_environment_id, left_folder,
                                       right_region_id, right_environment_id, right_folder):
    try:
        json_data = load_json_file(COMPARE_RESULT_PATH + "-9223372036284746972.json")

        # only_last_version = True
        # apply_filter_folders = True
        # left_root_obj = DirRootObject(left_region_id, left_environment_id, left_folder, only_last_version)
        # right_root_obj = DirRootObject(right_region_id, right_environment_id, right_folder, only_last_version)
        # root_hash_key = hash(left_root_obj) + hash(right_root_obj)
        # left_root_obj.update_root_hash_key(root_hash_key)
        # right_root_obj.update_root_hash_key(root_hash_key)
        # info_log("service", "diff_country_level compare_key:" + str(root_hash_key))
        #
        # if apply_filter_folders:
        #     dir_node_diff_obj = DirNodeDiffFilterObject(left_root_obj.dir_connect_obj, right_root_obj.dir_connect_obj,
        #                                                 left_root_obj.node_object, right_root_obj.node_object,
        #                                                 left_root_obj.filter_modules, right_root_obj.filter_modules)
        # else:
        #     dir_node_diff_obj = DirNodeDiffObject(left_root_obj.dir_connect_obj, right_root_obj.dir_connect_obj,
        #                                           left_root_obj.node_object, right_root_obj.node_object)
        # dir_node_diff_obj.diff()
        # json_data = CountryLevelDiffResultBuilder(left_root_obj, right_root_obj, root_hash_key).get_data()
        #
        # file_path = COMPARE_RESULT_PATH + "%s.%s" % (root_hash_key, KEY_JSON)
        # save_file(file_path, json.dumps(json_data))
        # info_log("service", "diff_country_level done")
        return json_data
    except Exception as e:
        raise e
