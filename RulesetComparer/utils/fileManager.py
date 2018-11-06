import os
import shutil
import glob
import json
from django.conf import settings
from codecs import open
from RulesetComparer.properties.config import get_compare_result_full_file_name

# codecs save file mode
SAVE_FILE_MODE_ADD = 'a'
SAVE_FILE_MODE_WRITE = 'w'
SAVE_FILE_MODE_READ = 'r'


def is_folder_exist(path):
    if os.path.isdir(path):
        return True
    else:
        return False


def create_folder(path):
    if not is_folder_exist(path):
        os.makedirs(path)


def clear_folder(path):
    if is_folder_exist(path):
        shutil.rmtree(path)


def save_compare_result_html(compare_key, content):
    file_name_with_path = get_compare_result_full_file_name("_html", compare_key)
    save_file(file_name_with_path, content)


def load_compare_result_html(compare_key):
    file_name_with_path = get_compare_result_full_file_name("_html", compare_key)
    file = load_file(file_name_with_path)
    return file


def save_compare_result_file(compare_key, data):
    file_name_with_path = get_compare_result_full_file_name("_json", compare_key)
    save_file(file_name_with_path, json.dumps(data))


def load_compare_result_file(compare_key):
    file_name_with_path = get_compare_result_full_file_name("_json", compare_key)
    with open(file_name_with_path) as json_file:
        data = json.load(json_file)
        return data


def save_file(file_name, content):
    save_file_with_setting(file_name, SAVE_FILE_MODE_WRITE, settings.UNICODE_ENCODING, content)


def save_file_with_setting(file_name, mode, format, content):
    file = open(file_name, mode, format)
    file.write(content)
    file.close()


def load_file(file_name):
    return load_file_with_setting(file_name, SAVE_FILE_MODE_READ, settings.UNICODE_ENCODING)


def load_file_with_setting(file_name, mode, format):
    return open(file_name, mode, format)


def load_file_in_folder(path, extension):
    name_filter = path + "*"+extension
    return [glob.glob(name_filter)]


def get_rule_name_list(path):
    rule_name_list = list()
    for file_name in os.listdir(path):
        full_path = path + "/" + file_name
        if os.path.isdir(full_path):
            continue

        file_name = file_name[:-4]
        rule_name_list.append(file_name)
    return rule_name_list
