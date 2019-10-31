import json

from RulesetComparer.properties.key import KEY_JSON
from RulesetComparer.utils.fileManager import create_folder, save_file, load_json_file, load_file
from shared_storage.properties.config import COMPARE_RESULT_PATH, COMPARE_FILE_PATH


def save_folder_file_diff_json(root_key, json_data):
    path = COMPARE_RESULT_PATH + "%s.%s" % (root_key, KEY_JSON)
    save_file(path, json.dumps(json_data))


def load_folder_file_diff_json(root_key):
    path = COMPARE_RESULT_PATH + "%s.%s" % (root_key, KEY_JSON)
    return load_json_file(path)


def save_file_diff_json(root_key, node_key, json_data):
    root_path = COMPARE_RESULT_PATH + root_key
    create_folder(root_path)

    file_path = root_path + "/%s.%s" % (node_key, KEY_JSON)
    save_file(file_path, json.dumps(json_data))


def load_file_diff_json(root_key, node_key):
    root_path = COMPARE_RESULT_PATH + root_key
    file_path = root_path + "/%s.%s" % (node_key, KEY_JSON)
    return load_json_file(file_path)


def save_file_detail_json(root_key, env_name, node_key, json_data):
    root_path = COMPARE_RESULT_PATH + root_key + "/" + env_name
    create_folder(root_path)

    file_path = root_path + "/%s.%s" % (node_key, KEY_JSON)
    save_file(file_path, json.dumps(json_data))


def load_file_detail_json(root_key, env_name, node_key):
    root_path = COMPARE_RESULT_PATH + root_key + "/" + env_name
    file_path = root_path + "/%s.%s" % (node_key, KEY_JSON)
    return load_json_file(file_path)


def load_file_content(root_key, environment, file_name):
    path = COMPARE_FILE_PATH + "%s/%s/%s" % (root_key, environment, file_name)
    return load_file(path)



