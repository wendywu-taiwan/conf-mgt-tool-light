from shared_storage.models import SharedStorageReportScheduler
from permission.utils.permission_manager import *


class UpdateReportSchedulerStatusParser:
    def __init__(self, json_data):
        self.task_id = json_data.get(KEY_TASK_ID)
        self.task = SharedStorageReportScheduler.objects.get(id=self.task_id)

        self.enable = json_data.get(KEY_ENABLE)
        if self.enable:
            self.enable = 1
        else:
            self.enable = 0
