import os, time, sys
import shutil
import glob
import json
import zipfile
import codecs
from django.conf import settings
from codecs import open
from RulesetComparer.properties.config import get_compare_result_full_file_name
from RulesetComparer.utils.logger import *
from pathlib import Path

# codecs save file mode
SAVE_FILE_MODE_ADD = 'a'
SAVE_FILE_MODE_WRITE = 'w'
SAVE_FILE_MODE_READ = 'r'
LOG_CLASS = "fileManager"
SECONDS_A_DAY = 86400


def is_folder_exist(path):
    if os.path.isdir(path):
        return True
    else:
        return False


def is_file_exist(file_name):
    file_path = Path(file_name)
    if file_path.is_file():
        return True
    else:
        return False


def create_folder(path):
    if not is_folder_exist(path):
        os.makedirs(path)


def clear_folder(path):
    if is_folder_exist(path):
        shutil.rmtree(path)


def clear_folder_over_days(folder_path, days, except_array):
    now = time.time()
    delete_files = []
    for file in os.listdir(folder_path):
        if except_array is not None and file in except_array:
            continue

        file_with_path = folder_path + "/" + file
        file_create_time = os.stat(file_with_path).st_mtime

        if file_create_time < now - days * SECONDS_A_DAY:
            if os.path.isfile(file_with_path):
                info_log(None, "delete file :" + file_with_path)
                delete_files.append(file)
                os.remove(os.path.join(folder_path, file))
            elif os.path.isdir(file_with_path):
                info_log(None, "delete folder :" + file_with_path)
                delete_files.append(file)
                clear_folder(file_with_path)
    return delete_files


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
    return load_json_file(file_name_with_path)


def save_auto_sync_pre_json_file(file_path, data):
    create_folder(file_path)
    file_name = get_file_name("_json", "pre")
    file_name_with_path = file_path + "/" + file_name
    save_file(file_name_with_path, json.dumps(data))


def load_auto_sync_pre_json_file(file_path):
    file_name = get_file_name("_json", "pre")
    file_name_with_path = file_path + "/" + file_name
    return load_json_file(file_name_with_path)


def load_json_file(file_path):
    if file_path is None:
        return None
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


def save_file(file_name, content):
    save_file_with_setting(file_name, SAVE_FILE_MODE_WRITE, settings.UNICODE_ENCODING, content)


def save_file_with_setting(file_name, mode, format, content):
    file = open(file_name, mode, format)
    file.write(content)
    file.close()


def load_file(file_name):
    if is_file_exist(file_name):
        return load_file_with_setting(file_name, SAVE_FILE_MODE_READ, settings.UNICODE_ENCODING)
    else:
        info_log(LOG_CLASS, " file not exist :" + file_name)
        return None


def archive_file(source_path, dst_path, dst_file):
    create_folder(dst_path)
    zip_handler = zipfile.ZipFile(dst_file, mode='w')
    for dirname, subdirs, files in os.walk(source_path):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            print("archive_file, resource path :" + absname)
            zip_handler.write(absname)
    zip_handler.close()


def archive_file_with_arcname(source_path, dst_path, dst_file, arcname_prefix):
    create_folder(dst_path)
    abs_src = os.path.abspath(source_path)

    zip_handler = zipfile.ZipFile(dst_file, mode='w')
    for dirname, subdirs, files in os.walk(source_path):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = arcname_prefix + absname[len(abs_src) + 1:]
            print("archive_file, resource path :" + absname)
            zip_handler.write(absname, arcname)
    zip_handler.close()


def load_file_with_setting(file_name, mode, format):
    fp = codecs.open(file_name, mode, format)
    return fp.read()


def load_file_in_folder(path, extension):
    name_filter = path + "*" + extension
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
