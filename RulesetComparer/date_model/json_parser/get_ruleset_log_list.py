from django.db.models import Q
from django.http import HttpResponseBadRequest

from RulesetComparer.models import RulesetLogGroup, RulesetLog
from permission.utils.permission_manager import *
from common.utils.utility import get_union, to_int_list


class GetRulesetLogListParser:
    DEFAULT_ORDER = "descend"
    DEFAULT_PAGE = 1
    DEFAULT_LIMIT = 10

    def __init__(self, user, json_data, new_filter=True):
        try:
            if json_data is HttpResponseBadRequest:
                self.filter_user_ids = []
                self.filter_environment_ids = []
                self.filter_countries_ids = []
                self.filter_keys = []
                self.order = self.DEFAULT_ORDER
                self.limit = self.DEFAULT_LIMIT
                self.page = self.DEFAULT_PAGE
            else:
                self.filter_user_ids = to_int_list(json_data.get("filter_user_ids"))
                self.filter_environment_ids = to_int_list(json_data.get("filter_environment_ids"))
                self.filter_countries_ids = to_int_list(json_data.get("filter_countries_ids"))
                self.filter_keys = json_data.get("filter_keys")
                self.order = json_data.get("order")
                self.page = int(json_data.get("page"))
                self.limit = json_data.get("limit")

            self.user = user
            self.enable_environment_ids = enable_environments(self.user.id, KEY_F_RULESET_LOG, KEY_M_RULESET)
            self.new_filter = new_filter

            self.order_descend = self.is_descend_order()
            self.log_group_query = Q(log_count__gt=0)
            self.log_query = Q()

            self.parse_user_query()
            self.parse_environment_query()
            self.parse_country_query()
            self.parse_ruleset_name_query()

            self.add_log_groups_result_query()
            self.log_filter = self.parse_log_filter()
            self.total_pages = self.parse_total_pages()
            self.check_page_within_total_pages()
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
        query = Q()
        if len(self.filter_environment_ids) == 0:
            query.add(Q(source_environment__in=self.enable_environment_ids), Q.AND)
            query.add(Q(target_environment__in=self.enable_environment_ids), Q.AND)
        else:
            union_list = get_union(self.enable_environment_ids, self.filter_environment_ids)
            if len(union_list) == 0:
                union_list = self.enable_environment_ids

            sub_query = Q()
            sub_query.add(Q(source_environment__in=union_list), Q.AND)
            sub_query.add(Q(target_environment__in=self.enable_environment_ids), Q.AND)
            query.add(sub_query, Q.OR)
            sub_query = Q()
            sub_query.add(Q(source_environment__in=self.enable_environment_ids), Q.AND)
            sub_query.add(Q(target_environment__in=union_list), Q.AND)
            query.add(sub_query, Q.OR)

        self.log_group_query.add(query, Q.AND)

    def parse_country_query(self):
        enable_country_ids = enable_environments_countries(self.user.id, self.enable_environment_ids)
        query = Q()
        if len(self.filter_countries_ids) == 0:
            query.add(Q(country_id__in=enable_country_ids), Q.AND)
        else:
            union_list = get_union(enable_country_ids, self.filter_countries_ids)
            if len(union_list) == 0:
                union_list = enable_country_ids
            query.add(Q(country_id__in=union_list), Q.AND)

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
        if len(log_group_ids) == 0:
            query.add(Q(ruleset_log_group=None), Q.OR)
        else:
            for id_obj in log_group_ids:
                log_group_id = id_obj.get("id")
                query.add(Q(ruleset_log_group=log_group_id), Q.OR)

        self.log_query.add(query, Q.AND)

    def add_log_groups_result_query(self):
        log_groups = RulesetLogGroup.objects.filter(self.log_group_query).values('id').order_by('-update_time')
        self.add_log_group_ids_query(log_groups)
        log_groups_query = log_groups.query

    def parse_log_filter(self):
        if self.order_descend:
            return RulesetLog.objects.filter(self.log_query).values().order_by(
                '-ruleset_log_group__update_time', '-id')
        else:
            return RulesetLog.objects.filter(self.log_query).values().order_by(
                'ruleset_log_group__update_time')

    def parse_total_pages(self):
        count = self.log_filter.count()

        remainder = count % self.limit

        if remainder > 0:
            return count // self.limit + 1
        else:
            return count // self.limit

    def check_page_within_total_pages(self):
        if self.new_filter is True or self.page > self.total_pages:
            self.page = 1

    def get_logs_query_result(self):
        last_item_index = self.page * self.limit
        first_item_index = last_item_index - self.limit

        return self.log_filter[first_item_index:last_item_index]
