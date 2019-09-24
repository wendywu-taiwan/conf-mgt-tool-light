import difflib
import json
from RulesetComparer.utils.fileManager import create_folder, save_file
from common.data_object.json_builder.key_content_diff_result import KeyContentDiffResultBuilder
from common.data_object.key_content_diff_object import KeyContentDiffObject
from shared_storage.data_object.json_builder.content_diff_result_builder import ContentDiffResultBuilder
from shared_storage.properties.config import COMPARE_RESULT_PATH, COMPARE_TYPE_BLACK_LIST
from RulesetComparer.utils.logger import *


class DiffFileTypeObject:

    def __init__(self, left_file_object, right_file_object, compare_key=None):
        self.left_file_object = left_file_object
        self.right_file_object = right_file_object
        self.file_type = self.left_file_object.file_type
        self.file_name = self.left_file_object.file_name
        self.left_contents_lines = self.left_file_object.file_content.splitlines()
        self.right_contents_lines = self.right_file_object.file_content.splitlines()
        self.compare_key = str(compare_key)

    def diff_file(self):
        if self.file_type in COMPARE_TYPE_BLACK_LIST:
            if self.left_file_object.file_size != self.right_file_object.file_size:
                return True
        else:
            if self.file_type == KEY_PROPERTIES:
                return self.diff_properties_file()
            else:
                return self.diff_string_content_file()

    def diff_properties_file(self):
        diff_object = KeyContentDiffObject(self.left_contents_lines, self.right_contents_lines)
        json = KeyContentDiffResultBuilder(self.file_name, self.left_file_object.file_path,
                                           self.right_file_object.file_path, diff_object.left_only_list,
                                           diff_object.right_only_list, diff_object.different_list_left,
                                           diff_object.common_list_left, diff_object.right_key_object_map).get_data()
        return json.get(COMPARE_RESULT_HAS_CHANGES)

    def diff_string_content_file(self):
        diff = difflib._mdiff(self.left_contents_lines, self.right_contents_lines)
        diff = list(diff)
        json = ContentDiffResultBuilder(self.file_name, self.left_file_object.file_path,
                                        self.right_file_object.file_path, diff).get_data()
        return json.get(COMPARE_RESULT_HAS_CHANGES)

    def save_json(self, json_data):
        if self.compare_key is None:
            error_log("DiffFileTypeObject, no compare key to save json file")
            return

        compare_key_folder_path = COMPARE_RESULT_PATH + self.compare_key
        create_folder(compare_key_folder_path)

        left_file_path = json_data.get(KEY_LEFT_FILE)
        right_file_path = json_data.get(KEY_RIGHT_FILE)

        file_compare_key = hash(left_file_path) + hash(right_file_path)
        json_data[KEY_COMPARE_HASH_KEY] = file_compare_key

        file_path = compare_key_folder_path + "/%s.%s" % (file_compare_key, KEY_JSON)
        save_file(file_path, json.dumps(json_data))
        return file_compare_key
