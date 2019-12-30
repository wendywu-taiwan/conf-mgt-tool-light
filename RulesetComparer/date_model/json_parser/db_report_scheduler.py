from RulesetComparer.date_model.json_parser.base_report_scheduler import BaseReportSchedulerParser


class DBReportSchedulerParser(BaseReportSchedulerParser):

    def __init__(self, scheduler, country_list, mail_content_type_list):
        try:
            BaseReportSchedulerParser.__init__(self, scheduler.next_proceed_time)
            self.task_id = scheduler.id
            self.base_env_id = scheduler.base_environment.id
            self.compare_env_id = scheduler.compare_environment.id
            self.module_id = scheduler.module.id
            self.country_list = self.parse_country(country_list)
            self.mail_content_type_list = self.parse_db_mail_content_type(mail_content_type_list)
            self.mail_list = self.get_mail_list(scheduler.mail_list)
            self.frequency_type = scheduler.frequency_type
            self.interval = scheduler.interval
            self.utc_time = self.get_utc_time(self.local_time)
            self.skip_ruleset_map = self.parse_skip_rulesets_map(scheduler.skip_rulesets.all())
        except BaseException as e:
            raise e

    def parse_skip_rulesets_map(self, skip_rulesets):
        data_map = {}
        for skip_ruleset_model in skip_rulesets:
            data_map[skip_ruleset_model.country.id] = self.parse_text_list(skip_ruleset_model.ruleset_list)
        return data_map

    def parse_country(self, country_id_list):
        return super().parse_country(country_id_list)

    def parse_db_mail_content_type(self, mail_content_type_list):
        return super().parse_db_mail_content_type(mail_content_type_list)

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
