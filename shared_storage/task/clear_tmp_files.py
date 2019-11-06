from RulesetComparer.task.base_clear_files import BaseClearFilesTask
from shared_storage.properties.config import *
from common.properties.mail_setting import SEND_CLEAR_FILES_MAIL


class ClearTmpFilesTask(BaseClearFilesTask):

    def __init__(self):
        BaseClearFilesTask.__init__(self)
        self.logger = "ClearTmpFilesTask"
        self.expired_day = 14
        self.delete_files_path = COMPARE_FILE_PATH
        self.mail_setting = SEND_CLEAR_FILES_MAIL
        self.not_removed_files_extension = ["__init__.py", "zip_file"]

    def run_task(self):
        super().run_task()

    def execute(self):
        super().execute()

    def on_task_success(self):
        super().on_task_success()

    def on_task_failure(self):
        super().on_task_failure()
