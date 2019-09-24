import pysftp
from permission.models import FTPClient, Environment, Country
from shared_storage.properties.config import COMPARE_FILE_PATH
from RulesetComparer.date_model.json_parser.auth_data import FTPAuthDataParser


class FTPConnectionObject:
    LOG_CLASS = "FTPConnectionObject"

    def __init__(self, host, port, account, password):
        try:
            self.host = host
            self.port = port
            self.account = account
            self.password = password
            self.sftp = None
            self.connect()
        except Exception as e:
            raise e

    def connect(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.sftp = pysftp.Connection(host=self.host, port=self.port, username=self.account, password=self.password,
                                      cnopts=cnopts)

    def disconnect(self):
        self.sftp.close()

    def get_path_list_dir(self, path):
        self.sftp.cwd(path)
        return self.sftp.listdir_attr()

    def get_path_file(self, file_path, file_name_with_extension):
        self.sftp.get(file_path, localpath=file_name_with_extension)
        f = open(file_name_with_extension, 'r')
        file_content = f.read().strip()
        f.close()
        return file_content


class SharedStorageConnectionObject(FTPConnectionObject):
    LOG_CLASS = "SharedStorageConnectionObject"

    def __init__(self, client_id, environment_id, folder_name, only_last_version):
        ftp_client = FTPClient.objects.get(id=client_id)
        self.environment = Environment.objects.get(id=environment_id)
        self.only_last_version = only_last_version
        self.compare_key = None

        auth_data = FTPAuthDataParser(self.environment.name, folder_name)
        FTPConnectionObject.__init__(self, ftp_client.url, ftp_client.port,
                                     auth_data.get_account(),
                                     auth_data.get_password())

    def set_compare_key(self, compare_key):
        self.compare_key = compare_key

    def get_path_list_dir(self, path):
        return super().get_path_list_dir(path)

    def get_path_file(self, file_path, file_name_with_extension):
        return super().get_path_file(file_path, file_name_with_extension)

    def get_latest_version(self, node_path):
        tmp_file = 'lastversion.dat'
        last_version_path = node_path + "/" + tmp_file
        self.sftp.get(last_version_path, localpath=tmp_file)
        f = open(tmp_file, 'r')
        last_version = f.read().strip()
        f.close()
        return last_version

    def get_file_contents(self, file_load_object):
        local_path = COMPARE_FILE_PATH + file_load_object.file_name
        self.sftp.get(file_load_object.file_path, localpath=local_path)
        try:
            f = open(local_path, 'r')
            file_content = f.read()
        except UnicodeDecodeError:
            f = open(local_path, 'rb')
            file_content = f.read()

        f.close()

        file_load_object.file_content = file_content
        return file_load_object
