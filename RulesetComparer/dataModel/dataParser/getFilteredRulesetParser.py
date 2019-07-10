from django.db.models import Q
from RulesetComparer.properties.config import *
from RulesetComparer.models import Environment, Country, RulesetLogGroup, RulesetLog


class GetFilteredRulesetParser:
    JSON_KEY_ENV_ID = "environment_id"
    JSON_KEY_COUNTRY_ID = "country_id"
    JSON_KEY_FILTER_KEYS = "filter_keys"

    def __init__(self, json_data):
        try:
            self.environment = Environment.objects.get(id=json_data[self.JSON_KEY_ENV_ID])
            self.country = Country.objects.get(id=json_data[self.JSON_KEY_COUNTRY_ID])
            self.filter_keys = json_data[self.JSON_KEY_FILTER_KEYS]
            self.is_git = self.is_git_env()
            self.log_groups = None
            self.logs_map = {}
            self.log_group_query = (Q(log_count__gt=0) & Q(updated__gt=0))
            self.log_query = Q()
            self.parse_environment_query()
            self.parse_country_query()
            self.parse_ruleset_name_query()
            self.parse_log_group_query()
            self.parse_logs_query()
        except BaseException as e:
            raise e

    def is_git_env(self):
        if self.environment.name == GIT["environment_name"]:
            return True
        else:
            return False

    def parse_environment_query(self):
        self.log_group_query.add(Q(target_environment=self.environment.id), Q.AND)

    def parse_country_query(self):
        self.log_group_query.add(Q(country=self.country.id), Q.AND)

    def parse_ruleset_name_query(self):
        if len(self.filter_keys) == 0:
            return

        query = Q()
        for key in self.filter_keys:
            query.add(Q(ruleset_name__contains=key), Q.AND)

        self.log_query.add(query, Q.AND)

    def parse_log_group_query(self):
        self.log_groups = RulesetLogGroup.objects.filter(self.log_group_query).values().order_by('-update_time')

    def parse_logs_query(self):
        for log_group in self.log_groups:
            query = Q()
            query.add(self.log_query, Q.AND)
            log_group_id = log_group.get(KEY_ID)
            query.add(Q(ruleset_log_group=log_group_id), Q.AND)
            query.add(Q(action__name=RULESET_UPDATE), Q.AND)
            logs = RulesetLog.objects.filter(query).values().order_by('-ruleset_log_group__update_time', '-id')
            if len(logs) != 0:
                self.logs_map[log_group.get(KEY_BACKUP_KEY)] = logs

    def get_log_group_result(self):
        return self.log_groups

    def get_logs_query_result(self, backup_key):
        return self.logs_map.get(backup_key)
