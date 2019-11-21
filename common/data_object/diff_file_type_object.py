import difflib
from common.data_object.json_builder.key_content_diff_result import KeyContentDiffResultBuilder
from common.data_object.key_content_diff_object import KeyContentDiffObject
from shared_storage.data_object.json_builder.content_diff_result_builder import ContentDiffResultBuilder
from shared_storage.data_object.json_builder.file_detail_builder import FileDetailBuilder
from shared_storage.properties.config import COMPARE_TYPE_WHITE_LIST
from shared_storage.utils.file_manager import save_file_diff_json, save_file_detail_json
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.fileManager import get_file_md5_from_file


class DiffFileTypeObject:

    def __init__(self, left_file_object, right_file_object, root_hash_key, node_hash_key):
        self.left_file_object = left_file_object
        self.right_file_object = right_file_object
        self.file_type = self.left_file_object.file_type
        self.file_name = self.left_file_object.file_name
        self.left_contents_lines = self.left_file_object.file_content.splitlines()
        self.right_contents_lines = self.right_file_object.file_content.splitlines()
        self.root_hash_key = str(root_hash_key)
        self.node_hash_key = str(node_hash_key)

    def diff_file(self):
        if self.file_type in COMPARE_TYPE_WHITE_LIST:
            if self.file_type == KEY_PROPERTIES:
                return self.diff_properties_file()
            else:
                return self.diff_string_content_file()
        else:
            return self.diff_file_md5()

    def diff_file_md5(self):
        left_md5 = get_file_md5_from_file(self.left_file_object.file_content_bytes)
        right_md5 = get_file_md5_from_file(self.right_file_object.file_content_bytes)
        left_json = FileDetailBuilder(self.left_file_object).get_data()
        right_json = FileDetailBuilder(self.right_file_object).get_data()
        self.save_detail_json(self.left_file_object.environment_name, left_json)
        self.save_detail_json(self.right_file_object.environment_name, right_json)

        return left_md5 != right_md5

    def diff_properties_file(self):
        diff_object = KeyContentDiffObject(self.left_contents_lines, self.right_contents_lines)
        json = KeyContentDiffResultBuilder(self.file_name, self.left_file_object.file_path,
                                           self.right_file_object.file_path,
                                           self.left_file_object.modification_time,
                                           self.right_file_object.modification_time,
                                           diff_object.left_only_list, diff_object.right_only_list,
                                           diff_object.different_list_left, diff_object.common_list_left,
                                           diff_object.right_key_object_map).get_data()
        self.save_diff_json(json)
        return json.get(COMPARE_RESULT_HAS_CHANGES)

    def diff_string_content_file(self):
        diff = difflib._mdiff(self.left_contents_lines, self.right_contents_lines)
        diff = list(diff)
        json = ContentDiffResultBuilder(self.file_name, self.left_file_object.file_path,
                                        self.right_file_object.file_path, self.left_file_object.modification_time,
                                        self.right_file_object.modification_time, diff).get_data()
        self.save_diff_json(json)
        return json.get(COMPARE_RESULT_HAS_CHANGES)

    def save_detail_json(self, environment_name, json_data):
        if self.root_hash_key is None:
            error_log("DiffFileTypeObject, no compare key to save json file")
            return

        save_file_detail_json(self.root_hash_key, environment_name, self.node_hash_key, json_data)

    def save_diff_json(self, json_data):
        if self.root_hash_key is None:
            error_log("DiffFileTypeObject, no compare key to save json file")
            return

        json_data[KEY_COMPARE_HASH_KEY] = self.node_hash_key
        save_file_diff_json(self.root_hash_key, self.node_hash_key, json_data)
