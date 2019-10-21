import pysftp
from permission.models import FTPRegion, FTPServer, Environment, Country
from shared_storage.properties.config import COMPARE_FILE_PATH
from RulesetComparer.date_model.json_parser.auth_data import FTPAuthDataParser
from RulesetComparer.utils.fileManager import load_path_file
from common.data_object.dir_connect_object import DirConnectObject


class FTPConnectionObject(DirConnectObject):
    LOG_CLASS = "FTPConnectionObject"

    def __init__(self, host, port, account, password):
        try:
            super().__init__()
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

    def get_path_file(self, file_path, save_path):
        self.sftp.get(file_path, localpath=save_path)
        f = open(save_path, 'r')
        file_content = f.read().strip()
        f.close()
        return file_content


class SharedStorageConnectionObject(FTPConnectionObject):
    LOG_CLASS = "SharedStorageConnectionObject"

    def __init__(self, region_id, environment_id, only_last_version):
        ftp_region = FTPRegion.objects.get(id=region_id)
        environment = Environment.objects.get(id=environment_id)
        ftp_server = FTPServer.objects.get(region=ftp_region, environment=environment)
        self.only_last_version = only_last_version

        auth_data = FTPAuthDataParser(ftp_server.environment.name, ftp_server.region.name)
        FTPConnectionObject.__init__(self, ftp_server.client.url, ftp_server.client.port,
                                     auth_data.get_account(),
                                     auth_data.get_password())

    def set_root_hash_key(self, root_hash_key):
        super().set_root_hash_key(root_hash_key)

    def get_path_list_dir(self, path):
        return super().get_path_list_dir(path)

    def get_path_file(self, file_path, save_path):
        return super().get_path_file(file_path, save_path)

    def get_latest_version(self, node_path):
        tmp_file = 'lastversion.dat'
        last_version_path = node_path + "/" + tmp_file
        last_version = self.get_path_file(last_version_path, COMPARE_FILE_PATH + tmp_file)
        return last_version

    def get_file_contents(self, file_load_object):
        self.sftp.get(file_load_object.file_path, localpath=file_load_object.local_path)
        file_load_object.set_file_content(load_path_file(file_load_object.local_path))
        return file_load_object
