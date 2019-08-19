from RulesetComparer.date_model.json_parser.permission import PermissionParser
from RulesetComparer.models import RulesetSyncUpScheduler
from permission.utils.permission_manager import *
from common.data_object.error.error import PermissionDeniedError


class DeleteSyncSchedulerParser(PermissionParser):
    def __init__(self, json_data, user):
        try:
            self.user = user
            self.task_id = json_data.get("id")
            self.task = RulesetSyncUpScheduler.objects.get(id=self.task_id)
            PermissionParser.__init__(self)
        except Exception as e:
            raise e

    def check_permission(self):
        function_id = Function.objects.get(name=KEY_F_REPORT_TASK).id

        for country_id_obj in self.task.country_list.values(KEY_ID):
            country_id = country_id_obj.get(KEY_ID)
            is_source_editable = is_editable(self.user.id, self.task.source_environment.id, country_id, function_id)
            is_target_editable = is_editable(self.user.id, self.task.target_environment.id, country_id, function_id)

            if is_source_editable is False or is_target_editable is False:
                raise PermissionDeniedError()
