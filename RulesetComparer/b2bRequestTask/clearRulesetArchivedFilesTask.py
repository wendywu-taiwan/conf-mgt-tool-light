from ConfigManageTool import settings
from RulesetComparer.properties import config
from RulesetComparer.b2bRequestTask.baseClearFilesTask import BaseClearFilesTask


class ClearRulesetArchivedFilesTask(BaseClearFilesTask):

    def __init__(self):
        BaseClearFilesTask.__init__(self)
        self.logger = "ClearRulesetArchivedFilesTask"
        self.expired_day = 1
        self.delete_files_path = config.get_full_file_path("rule_set_zip_file_path")
        self.mail_setting = config.SEND_CLEAR_FILES_MAIL
        self.not_removed_files_extension = ["__init__.py"]

    def run_task(self):
        super().run_task()

    def execute(self):
        super().execute()

    def on_task_success(self):
        super().on_task_success()

    def on_task_failure(self):
        super().on_task_failure()
