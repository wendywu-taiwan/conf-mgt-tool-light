from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import *


class SelectToDownloadFilterFolderBuilder(BaseBuilder):
    def __init__(self, type, name_list):
        try:
            self.name_list = name_list
            self.type = type
            self.folder_object_list = self.build_folder_object()
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def build_folder_object(self):
        folder_object_list = list()
        index = 1
        for name in self.name_list:
            folder_object = {
                "id": index,
                "name": name
            }
            index = index + 1
            folder_object_list.append(folder_object)
        return folder_object_list

    def __generate_data__(self):
        self.result_dict[KEY_TYPE] = self.type
        self.result_dict[KEY_DATA] = self.folder_object_list


class SelectToDownloadFilterModuleBuilder(SelectToDownloadFilterFolderBuilder):
    def __init__(self, name_list):
        try:
            SelectToDownloadFilterFolderBuilder.__init__(self, "module", name_list)
        except Exception as e:
            raise e


class SelectToDownloadFilterDirFolderBuilder(BaseBuilder):
    def __init__(self, folders):
        try:
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
        self.result_dict[KEY_TYPE] = "folder"
        self.result_dict[KEY_DATA] = self.folder_object_list


class SelectToCompareFilterDirFolderBuilder(SelectToDownloadFilterDirFolderBuilder):
    def __init__(self, side, folders):
        try:
            self.side = side
            SelectToDownloadFilterDirFolderBuilder.__init__(self, folders)
        except Exception as e:
            raise e

    def __generate_data__(self):
        super().__generate_data__()
        self.result_dict[KEY_TITLE] = "Folder"
        self.result_dict[KEY_SIDE] = self.side


class FolderObject:
    def __init__(self, index, folder_name):
        self.id = index
        self.folder_name = folder_name
