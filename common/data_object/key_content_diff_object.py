from common.data_object.key_content_line_object import KeyContentLineObject


class KeyContentDiffObject:
    def __init__(self, left_line_contents, right_line_contents):
        self.left_line_contents = left_line_contents
        self.right_line_contents = right_line_contents
        self.left_key_set = set()
        self.right_key_set = set()
        self.left_key_object_map = {}
        self.right_key_object_map = {}
        self.left_only_list = list()
        self.right_only_list = list()
        self.different_list_left = list()
        self.common_list_left = list()
        self.parse_line_contents(self.left_line_contents, self.left_key_set, self.left_key_object_map)
        self.parse_line_contents(self.right_line_contents, self.right_key_set, self.right_key_object_map)
        self.diff()
        self.has_different = self.has_different()

    def parse_line_contents(self, line_contents, key_set, key_object_map):
        index = 1
        for line in line_contents:
            self.add_key_value_line(key_set, key_object_map, index, line)
            index = index + 1

    @staticmethod
    def add_key_value_line(key_set, key_object_map, index, line_str):
        line_object = KeyContentLineObject(index, line_str)
        if line_object.empty_line:
            return
        key_set.add(line_object.key)
        key_object_map[line_object.key] = line_object

    def diff(self):
        left_only = list(set(self.left_key_set).difference(set(self.right_key_set)))
        right_only = list(set(self.right_key_set).difference(set(self.left_key_set)))

        self.add_object_to_list(self.left_key_object_map, left_only, self.left_only_list)
        self.add_object_to_list(self.right_key_object_map, right_only, self.right_only_list)

        union = list(set(self.left_key_set) & set(self.right_key_set))
        for key in union:
            left_line_object = self.left_key_object_map.get(key)
            right_line_object = self.right_key_object_map.get(key)
            if left_line_object.value != right_line_object.value:
                self.different_list_left.append(left_line_object)
            else:
                self.common_list_left.append(left_line_object)

        self.left_only_list.sort(key=lambda x: x.index, reverse=False)
        self.right_only_list.sort(key=lambda x: x.index, reverse=False)
        self.different_list_left.sort(key=lambda x: x.index, reverse=False)
        self.common_list_left.sort(key=lambda x: x.index, reverse=False)

    def has_different(self):
        if len(self.left_only_list) > 0 or len(self.right_only_list) > 0 or len(self.different_list_left) > 0:
            return True
        else:
            return False

    @staticmethod
    def add_object_to_list(object_map, key_list, object_list):
        for key in key_list:
            line_object = object_map.get(key)
            object_list.append(line_object)
