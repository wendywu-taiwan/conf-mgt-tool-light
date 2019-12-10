from common.models import FrequencyType
from common.data_object.json_parser.base_report_scheduler import BaseReportSchedulerParser
from ConfigManageTool.settings import CURRENT_REGION


class CreateReportSchedulerParser(BaseReportSchedulerParser):

    def __init__(self, json_data, host):
        BaseReportSchedulerParser.__init__(self, json_data.get("start_date_time"))
        self.request_host = host
        self.regional_tag = CURRENT_REGION
        self.task_id = json_data.get("id")
        self.left_data_center_id = json_data.get("left_data_center_id")
        self.right_data_center_id = json_data.get("right_data_center_id")
        self.left_environment_id = json_data.get("left_environment_id")
        self.right_environment_id = json_data.get("right_environment_id")
        self.left_folder = json_data.get("left_folder")
        self.right_folder = json_data.get("right_folder")
        self.mail_list = json_data.get("mail_list")
        self.frequency_type = FrequencyType.objects.get(id=json_data.get("frequency_type"))
        self.interval = int(json_data.get("interval"))
        # utc time for saving to database
        self.utc_time = self.get_utc_time(self.local_time)

    def frontend_time_to_date_time(self, start_date_time):
        return super().frontend_time_to_date_time(start_date_time)

    def get_utc_time(self, naive_local_time):
        return super().get_utc_time(naive_local_time)

    def get_local_time_shift_days(self, start_date_time):
        local_date_time = self.frontend_time_to_date_time(start_date_time)
        return super().get_local_time_shift_days(local_date_time)

    def local_date_time_bigger(self, local_date_time, current_date_time):
        return super().local_date_time_bigger(local_date_time, current_date_time)
