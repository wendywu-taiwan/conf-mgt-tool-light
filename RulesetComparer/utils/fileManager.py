import os
import shutil
import glob
from django.conf import settings
from codecs import open

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
