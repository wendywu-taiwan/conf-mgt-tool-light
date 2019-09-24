import traceback
import json
from shared_storage.data_object.dir_root_object import DirRootObject
from shared_storage.data_object.dir_node_diff_object import DirNodeDiffObject, DirNodeDiffFilterObject
from shared_storage.properties.config import COMPARE_RESULT_PATH
from shared_storage.services.diff_file_test import diff_content_test
from shared_storage.data_object.json_builder.country_level_diff_result_builder import CountryLevelDiffResultBuilder
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.fileManager import save_file


def diff_country_level():
    try:
        left_client_id = 2
        right_client_id = 2
        left_env_id = 5
        right_env_id = 6
        left_folder_name = "tw"
        right_folder_name = "tw"
        only_last_version = True
        apply_filter_folders = True
        left_root_obj = DirRootObject(left_client_id, left_env_id, left_folder_name, only_last_version)
        right_root_obj = DirRootObject(right_client_id, right_env_id, right_folder_name, only_last_version)
        compare_key = hash(left_root_obj) + hash(right_root_obj)
        info_log("service", "diff_country_level compare_key:" + str(compare_key))

        left_root_obj.update_compare_key(compare_key)
        right_root_obj.update_compare_key(compare_key)

        if apply_filter_folders:
            dir_node_diff_obj = DirNodeDiffFilterObject(left_root_obj.ftp_connect_obj, right_root_obj.ftp_connect_obj,
                                                        left_root_obj.node_object, right_root_obj.node_object,
                                                        left_root_obj.filter_modules, right_root_obj.filter_modules)
        else:
            dir_node_diff_obj = DirNodeDiffObject(left_root_obj.ftp_connect_obj, right_root_obj.ftp_connect_obj,
                                                  left_root_obj.node_object, right_root_obj.node_object)
        dir_node_diff_obj.diff()
        json_data = CountryLevelDiffResultBuilder(left_root_obj, right_root_obj, compare_key).get_data()

        file_path = COMPARE_RESULT_PATH + "%s.%s" % (compare_key, KEY_JSON)
        save_file(file_path, json.dumps(json_data))
        info_log("service", "diff_country_level done")
    except Exception as e:
        error_log(e)
        traceback.print_exc()


def diff_file():
    try:
        diff_content_test()
    except Exception as e:
        error_log(e)
        traceback.print_exc()
