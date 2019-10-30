from RulesetComparer.properties.key import KEY_FOLDER_NAME, GIT_NAME
from common.data_object.ftp_connect_object import SharedStorageConnectionObject
from common.data_object.git_connect_object import SharedStorageGitConnectObject
from common.data_object.json_builder.environment import EnvironmentsBuilder
from permission.models import Environment, FTPServer
from shared_storage.data_object.dir_root_object import DirRootObject
from shared_storage.data_object.json_parser.select_to_download_parser import SelectToDownloadFileListParser, \
    SelectToDownloadFilterResultParser
from shared_storage.data_object.dir_node_parse_object import DirNodeParseFilteredObject, \
    DirNodeParseFilteredLatestVersionParentObject
from shared_storage.data_object.json_builder.select_to_download_filterd_files_builder import \
    SelectToDownloadFilteredFilesBuilder
from shared_storage.data_object.node_object import NodeObject
from shared_storage.properties.config import COUNTRY_MODULE_MAP
from shared_storage.data_object.json_parser.filter_environment import \
    SelectToDownloadFilterEnvironmentParser
from shared_storage.data_object.json_builder.filter_environment import \
    SelectToDownloadFilterEnvironmentBuilder
from shared_storage.data_object.json_parser.filter_folder import \
    SelectToDownloadFilterFolderParser
from shared_storage.data_object.json_builder.filter_folder_builder import \
    SelectToDownloadFilterModuleBuilder, SelectToDownloadFilterDirFolderBuilder
from shared_storage.data_object.json_builder.select_to_download_file_list_builder import SelectToDownloadFileListBuilder


def get_region_environment_list(json_data):
    try:
        parser = SelectToDownloadFilterEnvironmentParser(json_data)
        environment_list = FTPServer.objects.filter(region__id=parser.region_id).values_list("environment_id",
                                                                                             flat=True)
        environments_json = EnvironmentsBuilder(ids=environment_list).get_data()
        result_json = SelectToDownloadFilterEnvironmentBuilder(environments_json).get_data()
        return result_json
    except Exception as e:
        raise e


def get_environment_dir_list(json_data):
    try:
        parser = SelectToDownloadFilterFolderParser(json_data)
        environment = Environment.objects.get(id=parser.environment_id)
        if environment.name == GIT_NAME:
            dir_connect_obj = SharedStorageGitConnectObject(False)
        else:
            dir_connect_obj = SharedStorageConnectionObject(parser.region_id, parser.environment_id, False)

        list_dir = dir_connect_obj.get_path_list_dir("")
        result_json = SelectToDownloadFilterDirFolderBuilder(list_dir).get_data()
        return result_json
    except Exception as e:
        raise e


def filter_second_folder(json_data):
    folder_name = json_data.get(KEY_FOLDER_NAME)
    second_folder_list = COUNTRY_MODULE_MAP[folder_name]
    result_json = SelectToDownloadFilterModuleBuilder(second_folder_list).get_data()
    return result_json


def filter_file_result(json_data):
    parser = SelectToDownloadFilterResultParser(json_data)
    # initial root node
    root_obj = DirRootObject(parser.region_id, parser.environment_id, parser.folder_name,
                             parser.only_latest_version)
    root_obj.update_root_hash_key(hash(root_obj))

    # parse node data to list
    if parser.only_latest_version:
        parse_obj = DirNodeParseFilteredLatestVersionParentObject(root_obj.dir_connect_obj, root_obj.node_object,
                                                                  [parser.module_name])
    else:
        parse_obj = DirNodeParseFilteredObject(root_obj.dir_connect_obj, root_obj.node_object, [parser.module_name])
    parse_obj.parse_nodes()

    # filter correspond node data to result list and download files
    result_json = SelectToDownloadFilteredFilesBuilder(root_obj, parser.filter_keys).get_data()
    return result_json


def file_list(json_data):
    parser = SelectToDownloadFileListParser(json_data)
    # initial root node
    root_obj = DirRootObject(parser.region_id, parser.environment_id, parser.folder_name,
                             parser.only_latest_version)
    root_obj.update_root_hash_key(hash(root_obj))

    # parse node data to list
    if parser.only_latest_version:
        parse_obj = DirNodeParseFilteredLatestVersionParentObject(root_obj.dir_connect_obj, root_obj.node_object,
                                                                  [parser.module_name])
    else:
        parse_obj = DirNodeParseFilteredObject(root_obj.dir_connect_obj, root_obj.node_object, [parser.module_name])
    parse_obj.parse_nodes()

    # filter correspond node data to result list and download files
    result_json = SelectToDownloadFileListBuilder(root_obj).get_data()
    return result_json
