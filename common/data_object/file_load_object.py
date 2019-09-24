class FileLoadObject:
    def __init__(self, file_name, file_path, file_type):
        self.file_name = file_name
        self.file_path = file_path
        self.file_type = file_type
        self.file_content = None

    def set_file_content(self, file_content):
        self.file_content = file_content
