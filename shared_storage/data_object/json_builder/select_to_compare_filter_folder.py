from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import *


class SelectToCompareFilterFolderBuilder(BaseBuilder):
    def __init__(self, side, folders):
        try:
            self.side = side
            self.folders = folders
            self.folder_object_list = self.build_folder_object()
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def build_folder_object(self):
        folder_object_list = list()
        index = 1
        for entry in self.folders:
            folder_object = {
                "id": index,
                "name": entry.filename
            }
            index = index + 1
            folder_object_list.append(folder_object)
        return folder_object_list

    def __generate_data__(self):
        self.result_dict[KEY_SIDE] = self.side
        self.result_dict[KEY_TITLE] = "Folder"
        self.result_dict[KEY_TYPE] = "folder"
        self.result_dict[KEY_DATA] = self.folder_object_list


class FolderObject:
    def __init__(self, index, folder_name):
        self.id = index
        self.folder_name = folder_name
