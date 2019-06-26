from django.db.models import Q


class GetRulesetLogListParser:
    def __init__(self, json_data):
        try:
            self.filter_user_ids = json_data.get("filter_user_ids")
            self.filter_environment_ids = json_data.get("filter_environment_ids")
            self.filter_countries_ids = json_data.get("filter_countries_ids")
            self.filter_keys = json_data.get("filter_keys")
            self.order = json_data.get("order")
            self.page = json_data.get("page")
            self.limit = json_data.get("limit")

            self.order_descend = self.is_descend_order()
            self.log_group_query = Q(log_count__gt=0)
            self.log_query = Q()

            self.parse_user_query()
            self.parse_environment_query()
            self.parse_country_query()
            self.parse_ruleset_name_query()
        except BaseException as e:
            raise e

    def is_descend_order(self):
        if self.order == "ascend":
            return False
        else:
            return True

    def parse_user_query(self):
        if len(self.filter_user_ids) == 0:
            return

        query = Q()
        for user_id in self.filter_user_ids:
            query.add(Q(author=user_id), Q.OR)

        self.log_group_query.add(query, Q.AND)

    def parse_environment_query(self):
        if len(self.filter_environment_ids) == 0:
            return

        query = Q()
        for environment_id in self.filter_environment_ids:
            query.add(Q(source_environment=environment_id), Q.OR)
            query.add(Q(target_environment=environment_id), Q.OR)

        self.log_group_query.add(query, Q.AND)

    def parse_country_query(self):
        if len(self.filter_countries_ids) == 0:
            return

        query = Q()
        for country_id in self.filter_countries_ids:
            query.add(Q(source_environment=country_id), Q.OR)

        self.log_group_query.add(query, Q.AND)

    def parse_ruleset_name_query(self):
        if len(self.filter_keys) == 0:
            return

        query = Q()
        for key in self.filter_keys:
            query.add(Q(ruleset_name__contains=key), Q.AND)

        self.log_query.add(query, Q.AND)

    def add_log_group_ids_query(self, log_group_ids):
        query = Q()
        for id_obj in log_group_ids:
            log_group_id = id_obj.get("id")
            query.add(Q(ruleset_log_group=log_group_id), Q.OR)

        self.log_query.add(query, Q.AND)
