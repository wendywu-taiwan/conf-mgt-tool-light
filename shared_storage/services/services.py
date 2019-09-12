import traceback
from shared_storage.data_object.dir_root_object import DirRootObject
from shared_storage.data_object.dir_node_diff_object import DirNodeDiffObject, DirNodeDiffFilterObject
from RulesetComparer.utils.logger import *


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
        if apply_filter_folders:
            dir_node_diff_obj = DirNodeDiffFilterObject(left_root_obj.ftp_connect_obj, right_root_obj.ftp_connect_obj,
                                                        left_root_obj.node_object, right_root_obj.node_object,
                                                        left_root_obj.filter_modules, right_root_obj.filter_modules)
        else:
            dir_node_diff_obj = DirNodeDiffObject(left_root_obj.ftp_connect_obj, right_root_obj.ftp_connect_obj,
                                                  left_root_obj.node_object, right_root_obj.node_object)
        dir_node_diff_obj.diff()
        left_json = left_root_obj.generate_json()
        right_json = right_root_obj.generate_json()
        info_log("service", "diff_country_level done")
    except Exception as e:
        error_log(e)
        traceback.print_exc()
