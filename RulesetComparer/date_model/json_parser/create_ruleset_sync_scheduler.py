from RulesetComparer.date_model.data_object.sync_action import SyncUpAction
from RulesetComparer.date_model.json_parser.base_report_scheduler import BaseReportSchedulerParser
from RulesetComparer.models import Environment
from RulesetComparer.date_model.json_parser.permission import PermissionParser
from common.models import FrequencyType
from permission.models import Module, Function
from permission.utils.permission_manager import *
from common.data_object.error.error import PermissionDeniedError


class CreateRulesetSyncSchedulerParser(BaseReportSchedulerParser, PermissionParser):
    def __init__(self, json_data, user):
        try:
            BaseReportSchedulerParser.__init__(self)
            self.user = user
            self.creator = user
            self.editor = user
            self.task_id = json_data.get("task_id")
            self.source_environment_id = json_data.get("source_environment_id")
            self.source_environment = Environment.objects.get(id=self.source_environment_id)

            self.target_environment_id = json_data.get("target_environment_id")
            self.target_environment = Environment.objects.get(id=self.target_environment_id)

            self.module = Module.objects.get(id=1)
            self.country_list = self.parse_country_id_list(json_data.get("country_list"))
            self.receiver_list = json_data.get("receiver_list")
            self.action_list = json_data.get("action_list")
            self.action = SyncUpAction(self.action_list)
            self.frequency_type = FrequencyType.objects.get(id=json_data.get("frequency_type"))
            self.interval = int(json_data.get("interval"))
            self.created_time = self.frontend_time_to_utc_time(json_data.get("created_time"))
            self.updated_time = self.frontend_time_to_utc_time(json_data.get("updated_time"))
            # time with timezone setting for task running
            self.local_time = self.get_local_time_shift_days(json_data.get("next_proceed_time"))
            # utc time for saving to database
            self.utc_time = self.get_utc_time(self.local_time)
            PermissionParser.__init__(self)
        except BaseException as e:
            raise e

    def set_task_id(self, task_id):
        self.task_id = task_id

    def parse_boolean_to_int(self, boolean):
        return super().parse_boolean_to_int(boolean)

    def parse_country_id_list(self, country_id_list):
        return super().parse_country_id_list(country_id_list)

    def frontend_time_to_utc_time(self, frontend_time):
        if frontend_time is not None:
            return super().frontend_time_to_utc_time(frontend_time)

    def frontend_time_to_date_time(self, start_date_time):
        return super().frontend_time_to_date_time(start_date_time)

    def get_utc_time(self, naive_local_time):
        return super().get_utc_time(naive_local_time)

    def get_local_time_shift_days(self, start_date_time):
        local_date_time = self.frontend_time_to_date_time(start_date_time)
        return super().get_local_time_shift_days(local_date_time)

    def local_date_time_bigger(self, local_date_time, current_date_time):
        return super().local_date_time_bigger(local_date_time, current_date_time)

    def check_permission(self):
        function_id = Function.objects.get(name=KEY_F_REPORT_TASK).id

        for country_id in self.country_list:
            is_base_editable = is_editable(self.user.id, self.source_environment_id, country_id, function_id)
            is_target_editable = is_editable(self.user.id, self.target_environment, country_id, function_id)

            if is_base_editable is False or is_target_editable is False:
                raise PermissionDeniedError()
