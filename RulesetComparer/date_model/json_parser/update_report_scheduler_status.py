from RulesetComparer.date_model.json_parser.permission import PermissionParser
from RulesetComparer.properties.key import *
from RulesetComparer.properties.message import PERMISSION_DENIED_MESSAGE
from RulesetComparer.models import ReportSchedulerInfo
from permission.models import Function
from permission.utils.permission_manager import *
from common.data_object.error.PermissionDeniedError import PermissionDeniedError


class UpdateReportSchedulerStatusParser(PermissionParser):
    def __init__(self, json_data, user):
        try:
            self.user = user
            self.task_id = json_data.get(KEY_TASK_ID)
            self.task = ReportSchedulerInfo.objects.get(id=self.task_id)

            self.enable = json_data.get(KEY_ENABLE)
            if self.enable:
                self.enable = 1
            else:
                self.enable = 0
            PermissionParser.__init__(self)
        except Exception as e:
            raise e

    def check_permission(self):
        function_id = Function.objects.get(name=KEY_F_REPORT_TASK).id

        for country_id_obj in self.task.country_list.values(KEY_ID):
            country_id = country_id_obj.get(KEY_ID)
            is_base_editable = is_editable(self.user.id, self.task.base_environment.id, country_id, function_id)
            is_target_editable = is_editable(self.user.id, self.task.compare_environment.id, country_id, function_id)

            if is_base_editable is False or is_target_editable is False:
                raise PermissionDeniedError(PERMISSION_DENIED_MESSAGE)
