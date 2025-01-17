import traceback
import json

from django.template.loader import render_to_string

from RulesetComparer.utils.mailSender import MailSender
from common.data_object.error.error import SharedStorageFTPServerConnectFailError
from permission.models import Environment
from shared_storage.data_object.dir_root_object import DirRootObject
from shared_storage.data_object.dir_node_diff_object import \
    DirNodeDiffFilteredLatestVersionParentObject as LatestVersionApplyObject
from shared_storage.data_object.dir_node_diff_object import DirNodeDiffLatestVersionParentObject as LatestVersionObject
from shared_storage.data_object.dir_node_diff_object import DirNodeDiffFilterObject as FilteredApplyObject

from shared_storage.data_object.dir_node_diff_object import DirNodeDiffObject, DirNodeDiffLatestVersionObject
from shared_storage.properties.config import COMPARE_RESULT_PATH, COMPARE_RESULT_MAIL_PATH
from shared_storage.data_object.json_builder.country_level_diff_result_builder import CountryLevelDiffResultBuilder
from shared_storage.data_object.json_builder.contry_level_diff_mail_result_builder import \
    CountryLevelDiffMailResultBuilder

from common.data_object.ftp_connect_object import SharedStorageConnectionObject
from common.data_object.git_connect_object import SharedStorageGitConnectObject
from common.properties.mail_setting import *
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.fileManager import save_file, load_json_file, create_folder
from permission.models import FTPRegion, FTPServer
from common.data_object.json_builder.environment import EnvironmentsBuilder
from common.data_object.json_builder.ftp_region import FTPRegionsBuilder
from shared_storage.data_object.json_builder.filter_environment import \
    SelectToCompareFilterEnvironmentBuilder
from shared_storage.data_object.json_parser.filter_environment import \
    SelectToCompareFilterEnvironmentParser
from shared_storage.data_object.json_builder.filter_folder_builder import \
    SelectToCompareFilterDirFolderBuilder
from shared_storage.data_object.json_parser.filter_folder import \
    SelectToCompareFilterFolderParser
from shared_storage.utils.file_manager import load_file_content


def get_active_region_list():
    region_id_list = FTPRegion.objects.filter(active=1).values_list("id", flat=True)
    data = FTPRegionsBuilder(ids=region_id_list).get_data()
    return data


def get_region_environment_list(json_data):
    parser = SelectToCompareFilterEnvironmentParser(json_data)
    environment_list = FTPServer.objects.filter(region__id=parser.region_id, environment__active=1).values_list(
        "environment_id", flat=True)
    environments_json = EnvironmentsBuilder(ids=environment_list).get_data()
    result_json = SelectToCompareFilterEnvironmentBuilder(parser.side, environments_json).get_data()
    return result_json


def get_environment_dir_list(json_data):
    parser = SelectToCompareFilterFolderParser(json_data)
    environment = Environment.objects.get(id=parser.environment_id)

    try:
        if environment.name == GIT_NAME:
            dir_connect_obj = SharedStorageGitConnectObject(False)
        else:
            dir_connect_obj = SharedStorageConnectionObject(parser.region_id, parser.environment_id, False)
    except Exception:
        error_log(traceback.format_exc())
        raise SharedStorageFTPServerConnectFailError

    list_dir = dir_connect_obj.get_path_list_dir("")
    result_json = SelectToCompareFilterDirFolderBuilder(parser.side, list_dir).get_data()
    return result_json


def compare_shared_storage_folder(left_region_id, left_environment_id, left_folder,
                                  right_region_id, right_environment_id, right_folder,
                                  send_mail, regional_tag=None, request_host=None):
    try:
        # json_data = load_json_file(COMPARE_RESULT_PATH + "-9223372036302886634.json")
        only_last_version = True
        left_root_obj = DirRootObject(left_region_id, left_environment_id, left_folder, only_last_version)
        right_root_obj = DirRootObject(right_region_id, right_environment_id, right_folder, only_last_version)

        root_hash_key = hash(left_root_obj)
        left_root_obj.update_root_hash_key(root_hash_key)
        right_root_obj.update_root_hash_key(root_hash_key)
        info_log("service", "compare_shared_storage_folder compare_key:" + str(root_hash_key))

        if left_root_obj.filter_modules is None:
            apply_filter_folders = False
        else:
            apply_filter_folders = True

        if apply_filter_folders and only_last_version:
            dir_diff_obj = LatestVersionApplyObject(left_root_obj.dir_connect_obj, right_root_obj.dir_connect_obj,
                                                    left_root_obj.node_object, right_root_obj.node_object,
                                                    left_root_obj.filter_modules, right_root_obj.filter_modules)
        elif apply_filter_folders:
            dir_diff_obj = FilteredApplyObject(left_root_obj.dir_connect_obj, right_root_obj.dir_connect_obj,
                                               left_root_obj.node_object, right_root_obj.node_object,
                                               left_root_obj.filter_modules, right_root_obj.filter_modules)
        elif only_last_version:
            dir_diff_obj = LatestVersionObject(left_root_obj.dir_connect_obj, right_root_obj.dir_connect_obj,
                                               left_root_obj.node_object, right_root_obj.node_object)
        else:
            dir_diff_obj = DirNodeDiffObject(left_root_obj.dir_connect_obj, right_root_obj.dir_connect_obj,
                                             left_root_obj.node_object, right_root_obj.node_object)
        dir_diff_obj.diff()
        json_data = CountryLevelDiffResultBuilder(left_root_obj, right_root_obj, root_hash_key).get_data()
        save_compare_result_page_json(json_data, root_hash_key)
        info_log("service", "compare_shared_storage_folder done")

        if not send_mail:
            return json_data
        else:
            mail_data = CountryLevelDiffMailResultBuilder(left_root_obj, right_root_obj, root_hash_key).get_data()
            mail_data[KEY_REQUEST_HOST] = request_host
            mail_data[KEY_URL_REGIONAL_TAG] = regional_tag
            save_compare_result_mail_json(mail_data, root_hash_key)
            return mail_data
    except Exception as e:
        raise e


def send_shared_storage_compare_result_mail(json, mail_list=None):
    mail_sender = MailSender(SHARED_FOLDER_COMPARE_MAIL_SETTING)
    folder = json.get(KEY_LEFT_FOLDER)
    left_region = json.get(KEY_LEFT_REGION)
    right_region = json.get(KEY_RIGHT_REGION)
    left_environment = json.get(KEY_LEFT_ENVIRONMENT)
    right_environment = json.get(KEY_RIGHT_ENVIRONMENT)
    left_env_info = left_region.get(KEY_NAME) + " " + left_environment.get(KEY_NAME)
    right_env_info = right_region.get(KEY_NAME) + " " + right_environment.get(KEY_NAME)

    # generate subject
    subject = SHARED_FOLDER_COMPARE_MAIL_SETTING.get(
        "title") + " for " + folder + " - " + left_env_info + " <> " + right_env_info

    # generate mail content
    html_content = render_to_string('shared_storage_compare_info_mail_content.html', json)

    if mail_list is None:
        mail_list = SHARED_FOLDER_COMPARE_MAIL_SETTING.get("receivers")

    mail_sender.set_receiver(mail_list)
    mail_sender.compose_msg(subject, None, html_content)
    mail_sender.send()
    mail_sender.quit()
    info_log("service", "send_shared_storage_compare_result_mail done")


def save_compare_result_page_json(json_data, root_hash_key):
    save_compare_result_json(json_data, root_hash_key, COMPARE_RESULT_PATH)


def save_compare_result_mail_json(json_data, root_hash_key):
    save_compare_result_json(json_data, root_hash_key, COMPARE_RESULT_MAIL_PATH)


def save_compare_result_json(json_data, root_hash_key, path_key):
    file_path = path_key + "%s.%s" % (root_hash_key, KEY_JSON)
    create_folder(path_key)
    save_file(file_path, json.dumps(json_data))
