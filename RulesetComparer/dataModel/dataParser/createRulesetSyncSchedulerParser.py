from RulesetComparer.dataModel.dataObject.syncUpAction import SyncUpAction
from RulesetComparer.dataModel.dataParser.baseReportSchedulerParser import BaseReportSchedulerParser
from RulesetComparer.utils.modelManager import get_default_module
from RulesetComparer.models import Environment


class CreateRulesetSyncSchedulerParser(BaseReportSchedulerParser):

    def __init__(self, json_data):
        try:
            BaseReportSchedulerParser.__init__(self)
            self.task_id = json_data.get("task_id")
            self.source_environment_id = json_data.get("source_environment_id")
            self.source_environment = Environment.objects.get(id=self.source_environment_id)

            self.target_environment_id = json_data.get("target_environment_id")
            self.target_environment = Environment.objects.get(id=self.target_environment_id)

            self.module = get_default_module()
            self.country_list = self.parse_country_id_list(json_data.get("country_list"))
            self.receiver_list = json_data.get("receiver_list")
            self.action_list = json_data.get("action_list")
            self.action = SyncUpAction(self.action_list)
            self.interval_hour = int(json_data.get("interval_hour"))
            self.backup = self.parse_boolean_to_int(json_data.get("backup"))
            # time with timezone setting for task running
            self.local_time = self.get_local_time_shift_days(json_data.get("next_proceed_time"))
            # utc time for saving to database
            self.utc_time = self.get_utc_time(self.local_time)
        except BaseException as e:
            raise e

    def set_task_id(self, task_id):
        self.task_id = task_id

    def parse_boolean_to_int(self, boolean):
        return super().parse_boolean_to_int(boolean)

    def parse_country_id_list(self, country_id_list):
        return super().parse_country_id_list(country_id_list)

    def frontend_time_to_date_time(self, start_date_time):
        return super().frontend_time_to_date_time(start_date_time)

    def get_utc_time(self, naive_local_time):
        return super().get_utc_time(naive_local_time)

    def get_local_time_shift_days(self, start_date_time):
        local_date_time = self.frontend_time_to_date_time(start_date_time)
        return super().get_local_time_shift_days(local_date_time)

    def local_date_time_bigger(self, local_date_time, current_date_time):
        return super().local_date_time_bigger(local_date_time, current_date_time)
