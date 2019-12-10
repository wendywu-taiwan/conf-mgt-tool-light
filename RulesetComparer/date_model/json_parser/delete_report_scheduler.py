from RulesetComparer.date_model.json_parser.permission import PermissionParser
from RulesetComparer.models import ReportSchedulerInfo
from permission.models import Country
from permission.utils.permission_manager import *
from common.data_object.error.error import PermissionDeniedError


class DeleteReportSchedulerParser():
    def __init__(self, json_data, user):
        self.user = user
        self.task_id = json_data.get("id")
        self.scheduler = ReportSchedulerInfo.objects.get(id=self.task_id)
        self.country_id_list = self.parse_country_list(self.scheduler.country_list.values(KEY_ID))
        self.base_env_id = self.scheduler.base_environment.id
        self.compare_env_id = self.scheduler.compare_environment.id

    @staticmethod
    def parse_country_list(country_id_list):
        country_list = list()
        for country_id_map in country_id_list:
            country = Country.objects.get(id=country_id_map['id'])
            country_list.append(country)
        return country_list
