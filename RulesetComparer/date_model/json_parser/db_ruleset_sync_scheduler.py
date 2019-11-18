from RulesetComparer.date_model.data_object.sync_action import SyncUpAction
from RulesetComparer.date_model.json_parser.base_report_scheduler import BaseReportSchedulerParser
from RulesetComparer.utils.modelManager import get_default_module


class DBRulesetSyncSchedulerParser(BaseReportSchedulerParser):

    def __init__(self, scheduler, country_list):
        try:
            BaseReportSchedulerParser.__init__(self, scheduler.next_proceed_time)
            self.task_id = scheduler.id
            self.source_environment_id = scheduler.source_environment.id
            self.source_environment = scheduler.source_environment
            self.target_environment_id = scheduler.target_environment.id
            self.target_environment = scheduler.target_environment
            self.module = get_default_module()
            self.country_list = self.parse_country(country_list)
            self.receiver_list = self.get_mail_list(scheduler.mail_list)
            self.action_list = self.get_action_list(scheduler.action_list)
            self.action = SyncUpAction(self.action_list)
            self.frequency_type = scheduler.frequency_type
            self.interval = scheduler.interval
            self.enable = self.parse_int_to_boolean(scheduler.enable)
            # utc time for saving to database
            self.utc_time = self.get_utc_time(self.local_time)
        except BaseException as e:
            raise e

    def parse_country(self, country_id_list):
        return super().parse_country(country_id_list)

    def get_mail_list(self, receiver_list):
        return super().get_mail_list(receiver_list)

    def get_action_list(self, action_list):
        return super().parse_text_list(action_list)

    def parse_int_to_boolean(self, int_value):
        return super().parse_int_to_boolean(int_value)

    def frontend_time_to_utc_time(self, frontend_time):
        if frontend_time is not None:
            return super().frontend_time_to_utc_time(frontend_time)

    def get_local_time_shift_days(self, start_date_time):
        local_date_time = self.db_time_to_date_time(start_date_time)
        return super().get_local_time_shift_days(local_date_time)

    def db_time_to_date_time(self, start_date_time):
        return super().db_time_to_date_time(start_date_time)
