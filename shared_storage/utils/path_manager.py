from shared_storage.properties.config import COMPARE_FILE_PATH


def get_download_file_folder_path(root_key, environment_name):
    return COMPARE_FILE_PATH + root_key + "/" + environment_name


def get_download_file_path(root_key, environment_name, file_name):
    return COMPARE_FILE_PATH + root_key + "/" + environment_name + "/" + file_name
