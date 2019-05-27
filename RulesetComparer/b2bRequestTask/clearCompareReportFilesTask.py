from RulesetComparer.properties import config
from RulesetComparer.b2bRequestTask.baseClearFilesTask import BaseClearFilesTask


class ClearCompareReportFilesTask(BaseClearFilesTask):

    def __init__(self):
        BaseClearFilesTask.__init__(self)
        self.logger = "ClearCompareResultFilesTask"
        self.expired_day = 3
        self.delete_files_path = config.get_full_file_path("compare_result")
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
