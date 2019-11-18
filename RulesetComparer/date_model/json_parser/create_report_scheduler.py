from RulesetComparer.date_model.json_parser.base_report_scheduler import BaseReportSchedulerParser
from RulesetComparer.date_model.json_parser.permission import PermissionParser
from permission.utils.permission_manager import *
from common.models import FrequencyType


class CreateReportSchedulerTaskParser(BaseReportSchedulerParser, PermissionParser):

    def __init__(self, json_data, user):
        try:
            BaseReportSchedulerParser.__init__(self, json_data.get("start_date_time"))
            self.user = user
            self.task_id = json_data.get("id")
            self.base_env_id = json_data.get("base_environment_id")
            self.compare_env_id = json_data.get("compare_environment_id")
            self.module_id = json_data.get("module_id")
            self.module_id = 1
            self.country_list = self.parse_country_id_list(json_data.get("country_list"))
            self.mail_content_type_list = self.parse_mail_content_type_list(json_data.get("mail_content_type_list"))
            self.mail_list = json_data.get("mail_list")
            self.frequency_type = FrequencyType.objects.get(id=json_data.get("frequency_type"))
            self.interval = int(json_data.get("interval"))
            # utc time for saving to database
            self.utc_time = self.get_utc_time(self.local_time)
            PermissionParser.__init__(self)
        except BaseException as e:
            raise e

    def parse_country_id_list(self, country_id_list):
        return super().parse_country_id_list(country_id_list)

    def parse_mail_content_type_list(self, mail_content_type_list):
        return super().parse_mail_content_type_list(mail_content_type_list)

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
            is_base_editable = is_editable(self.user.id, self.base_env_id, country_id, function_id)
            is_target_editable = is_editable(self.user.id, self.compare_env_id, country_id, function_id)

            if is_base_editable is False or is_target_editable is False:
                raise PermissionDeniedError()
