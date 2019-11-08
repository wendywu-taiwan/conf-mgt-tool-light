import traceback

from RulesetComparer.properties.key import KEY_FOLDER_NAME, GIT_NAME
from RulesetComparer.utils.logger import error_log
from common.data_object.error.error import SharedStorageFolderNotFoundError, SharedStorageFTPServerConnectFailError
from common.data_object.ftp_connect_object import SharedStorageConnectionObject
from common.data_object.git_connect_object import SharedStorageGitConnectObject
from common.data_object.json_builder.environment import EnvironmentsBuilder
from permission.models import Environment, FTPServer
from shared_storage.data_object.dir_root_object import DirRootObject
from shared_storage.data_object.dir_root_download_object import DirRootServerDownloadObject, DirRootGitDownloadObject, \
    DirRootExistDownloadObject
from shared_storage.data_object.json_parser.select_to_download_parser import SelectToDownloadFileListParser, \
    SelectToDownloadFilterResultParser
from shared_storage.data_object.dir_node_parse_object import DirNodeParseFilteredObject
from shared_storage.data_object.json_builder.select_to_download_filterd_files_builder import \
    SelectToDownloadFilteredFilesBuilder
from shared_storage.properties.config import COUNTRY_MODULE_MAP, FILTER_MODULE_FOLDER
from shared_storage.data_object.json_parser.filter_environment import \
    SelectToDownloadFilterEnvironmentParser
from shared_storage.data_object.json_builder.filter_environment import \
    SelectToDownloadFilterEnvironmentBuilder
from shared_storage.data_object.json_parser.filter_folder import \
    SelectToDownloadFilterFolderParser, SelectToDownloadFilterLatestVersionFolderParser
from shared_storage.data_object.json_builder.filter_folder_builder import \
    SelectToDownloadFilterModuleBuilder, SelectToDownloadFilterDirFolderBuilder, \
    SelectToDownloadFilterLatestVersionBuilder
from shared_storage.data_object.json_builder.select_to_download_file_list_builder import SelectToDownloadFileListBuilder
from shared_storage.data_object.json_parser.download_files import DownloadFilesParser, DownloadExistFilesParser
from shared_storage.task.download_server_file_task import DownloadServerFileTask


def get_region_environment_list(json_data):
    try:
        parser = SelectToDownloadFilterEnvironmentParser(json_data)
        environment_list = FTPServer.objects.filter(region__id=parser.region_id, environment__active=1).values_list(
            "environment_id", flat=True)
        environments_json = EnvironmentsBuilder(ids=environment_list).get_data()
        result_json = SelectToDownloadFilterEnvironmentBuilder(environments_json).get_data()
        return result_json
    except Exception as e:
        raise e


def get_environment_dir_list(json_data):
    parser = SelectToDownloadFilterFolderParser(json_data)
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
    result_json = SelectToDownloadFilterDirFolderBuilder("folder", list_dir).get_data()
    return result_json


def filter_second_folder(json_data):
    folder_name = json_data.get(KEY_FOLDER_NAME)
    second_folder_list = FILTER_MODULE_FOLDER
    result_json = SelectToDownloadFilterModuleBuilder(second_folder_list).get_data()
    return result_json


def filter_latest_version_folder(json_data):
    parser = SelectToDownloadFilterLatestVersionFolderParser(json_data)
    environment = Environment.objects.get(id=parser.environment_id)
    try:
        if environment.name == GIT_NAME:
            dir_connect_obj = SharedStorageGitConnectObject(False)
            list_dir = dir_connect_obj.get_path_list_dir(parser.git_full_path)
        else:
            dir_connect_obj = SharedStorageConnectionObject(parser.region_id, parser.environment_id, False)
            list_dir = dir_connect_obj.get_path_list_dir(parser.full_path)
    except FileNotFoundError:
        raise SharedStorageFolderNotFoundError
    result_json = SelectToDownloadFilterLatestVersionBuilder(list_dir).get_data()

    return result_json


def filter_file_result(json_data):
    parser = SelectToDownloadFilterResultParser(json_data)
    root_obj = parse_files(parser)
    # filter correspond node data to result list and download files
    result_json = SelectToDownloadFilteredFilesBuilder(root_obj, parser.filter_keys).get_data()
    return result_json


def file_list(json_data):
    parser = SelectToDownloadFileListParser(json_data)
    root_obj = parse_files(parser)
    # filter correspond node data to result list and download files
    result_json = SelectToDownloadFileListBuilder(root_obj).get_data()
    return result_json


def parse_files(parser):
    root_obj = DirRootObject(parser.region_id, parser.environment_id, parser.module_path,
                             parser.only_latest_version)
    root_obj.update_root_hash_key(hash(root_obj))

    if parser.only_latest_version:
        latest_version = root_obj.dir_connect_obj.get_latest_version(root_obj.node_object.path)
        parser.latest_version_folder = latest_version

    parse_obj = DirNodeParseFilteredObject(root_obj.dir_connect_obj, root_obj.node_object,
                                           [parser.latest_version_folder])
    parse_obj.parse_nodes()
    return root_obj


def download_files(json_data):
    parser = DownloadFilesParser(json_data)
    if parser.environment.name == GIT_NAME:
        root_obj = DirRootGitDownloadObject(parser.region_id, parser.environment_id, parser.file_path_list)
    else:
        root_obj = DirRootServerDownloadObject(parser.region_id, parser.environment_id, parser.file_path_list)
    file_object_list = root_obj.download_node_files()
    task = DownloadServerFileTask(file_object_list)
    return task.zip_file_full_path


def download_exist_files(json_data):
    parser = DownloadExistFilesParser(json_data)
    if parser.environment.name == GIT_NAME:
        root_obj = DirRootGitDownloadObject(parser.region_id, parser.environment_id, parser.file_path_list)
    else:
        root_obj = DirRootExistDownloadObject(parser.region_id, parser.environment_id, parser.file_path_list,
                                              parser.root_hash_key)
    file_object_list = root_obj.download_node_files()
    task = DownloadServerFileTask(file_object_list)
    return task.zip_file_full_path
