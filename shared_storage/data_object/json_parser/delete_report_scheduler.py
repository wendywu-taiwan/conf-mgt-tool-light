from shared_storage.models import SharedStorageReportScheduler


class DeleteReportSchedulerParser:
    def __init__(self, json_data):
        self.task_id = json_data.get("id")
        self.task = SharedStorageReportScheduler.objects.get(id=self.task_id)
