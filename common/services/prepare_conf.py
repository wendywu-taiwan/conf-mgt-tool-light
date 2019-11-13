from common.properties.config import SETTING_PATH
from shutil import copyfile
from RulesetComparer.utils.fileManager import clear_folder


def prepare_conf(file_name):
    setting_path = SETTING_PATH
    file_path = setting_path + file_name
    copied_full_path = setting_path + "settings.py"
    copyfile(file_path, copied_full_path)
