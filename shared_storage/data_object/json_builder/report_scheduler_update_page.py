from RulesetComparer.utils.logger import *
from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleSharedStorageBuilder
from common.data_object.json_builder.frequency_type import FrequencyTypesBuilder
from common.models import FrequencyType
from shared_storage.models import SharedStorageReportScheduler
from shared_storage.data_object.json_builder.shared_storage_report_scheduler import SharedStorageReportSchedulerBuilder


class ReportSchedulerUpdatePageBuilder(AdminConsoleSharedStorageBuilder):

    def __init__(self, user, visible_data, scheduler_id):
        self.regions_data = visible_data
        self.frequency_types = FrequencyTypesBuilder(FrequencyType.objects.all()).get_data()
        self.scheduler = SharedStorageReportScheduler.objects.get(id=scheduler_id)
        AdminConsoleSharedStorageBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[KEY_REGIONS] = self.regions_data
        self.result_dict[KEY_FREQUENCY_TYPES] = self.frequency_types
        self.result_dict[SCHEDULER_DATA] = SharedStorageReportSchedulerBuilder(None, self.scheduler).get_data()
