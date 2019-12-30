from RulesetComparer.date_model.json_parser.permission import PermissionParser
from permission.utils.permission_manager import *
from permission.models import Country
from common.models import FrequencyType
from common.data_object.json_parser.base_report_scheduler import BaseReportSchedulerParser


class CreateReportSchedulerParser(BaseReportSchedulerParser):

    def __init__(self, json_data, user):
        try:
            BaseReportSchedulerParser.__init__(self, json_data.get("start_date_time"))
            self.user = user
            self.task_id = json_data.get("id")
            self.base_env_id = json_data.get("base_environment_id")
            self.compare_env_id = json_data.get("compare_environment_id")
            self.module = Module.objects.get(name=KEY_M_RULESET)
            self.module_id = self.module.id
            self.country_list = self.parse_country_id_list(json_data.get("country_list"))
            self.mail_content_type_list = self.parse_mail_content_type_list(json_data.get("mail_content_type_list"))
            self.mail_list = json_data.get("mail_list")
            self.frequency_type = FrequencyType.objects.get(id=json_data.get("frequency_type"))
            self.interval = int(json_data.get("interval"))
            self.display_name = json_data.get("display_name")
            self.skip_ruleset_list = self.parse_skip_rulesets_list(json_data.get("skip_rulesets"))
            self.skip_ruleset_map = self.parse_skip_rulesets_map(json_data.get("skip_rulesets"))
            # utc time for saving to database
            self.utc_time = self.get_utc_time(self.local_time)
        except BaseException as e:
            raise e

    @staticmethod
    def parse_skip_rulesets_list(json_data):
        data_list = list()
        for country_json in json_data:
            country = Country.objects.get(id=country_json.get("country_id"))
            ruleset_list = country_json.get("ruleset_list")
            country_tuple = tuple([country, ruleset_list])
            data_list.append(country_tuple)
        return data_list

    @staticmethod
    def parse_skip_rulesets_map(json_data):
        data_map = {}
        for country_json in json_data:
            country_id = country_json.get("country_id")
            ruleset_list = country_json.get("ruleset_list")
            data_map[country_id] = ruleset_list
        return data_map

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
