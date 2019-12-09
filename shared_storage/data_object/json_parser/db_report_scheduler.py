from common.data_object.json_parser.base_report_scheduler import BaseReportSchedulerParser


class DBReportSchedulerParser(BaseReportSchedulerParser):

    def __init__(self, scheduler):
        try:
            BaseReportSchedulerParser.__init__(self, scheduler.next_proceed_time)
            self.task_id = scheduler.id
            self.left_data_center_id = scheduler.left_data_center.id
            self.right_data_center_id = scheduler.right_data_center.id
            self.left_environment_id = scheduler.left_environment.id
            self.right_environment_id = scheduler.right_environment.id
            self.left_folder = scheduler.left_folder
            self.right_folder = scheduler.right_folder
            self.mail_list = self.get_mail_list(scheduler.mail_list)
            self.frequency_type = scheduler.frequency_type
            self.interval = scheduler.interval
            self.utc_time = self.get_utc_time(self.local_time)
        except BaseException as e:
            raise e

    def db_time_to_date_time(self, start_date_time):
        return super().db_time_to_date_time(start_date_time)

    def get_utc_time(self, naive_local_time):
        return super().get_utc_time(naive_local_time)

    def local_date_time_bigger(self, local_date_time, current_date_time):
        return super().local_date_time_bigger(local_date_time, current_date_time)

    def get_local_time_shift_days(self, start_date_time):
        local_date_time = self.db_time_to_date_time(start_date_time)
        return super().get_local_time_shift_days(local_date_time)

    def get_mail_list(self, receiver_list):
        return super().get_mail_list(receiver_list)
