import os
import stat

from RulesetComparer.properties.key import KEY_FOLDER, KEY_OTHERS


class FileEntryObject:
    def __init__(self, file_path, filename):
        self.entry = os.stat(file_path)
        self.st_mode = self.entry.st_mode
        self.st_size = self.entry.st_size
        self.st_mtime = self.entry.st_mtime
        self.filename = filename
        self.type = self.parse_type()

    def parse_type(self):
        if self.st_mode is None or stat.S_ISDIR(self.st_mode):
            return KEY_FOLDER
        else:
            try:
                array = self.filename.split(".")
                return array[1]
            except IndexError:
                return KEY_OTHERS
