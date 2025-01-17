from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleRulesetBuilder
from RulesetComparer.models import RulesetLogGroup
from common.data_object.json_builder.user import UserBuilder
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.country import CountryBuilder
from permission.models import Country
from permission.utils.permission_manager import *


class RulesetLogListResultBuilder(AdminConsoleRulesetBuilder):
    def __init__(self, user, parser, ruleset_log_list):
        try:
            self.user = user
            self.parser = parser
            self.ruleset_log_list = ruleset_log_list
            self.enable_environment_ids = enable_environments(self.user.id, KEY_F_RULESET_LOG, KEY_M_RULESET)

            AdminConsoleRulesetBuilder.__init__(self, user)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = {
            KEY_RULESET_LOG_LIST: self.ruleset_log_list,
            KEY_USERS: self.get_users(),
            KEY_ENVIRONMENTS: self.get_environments(),
            KEY_COUNTRIES: self.get_countries(),
            KEY_FILTER_USER_IDS: self.parser.filter_user_ids,
            KEY_FILTER_ENVIRONMENT_IDS: self.parser.filter_environment_ids,
            KEY_FILTER_COUNTRIES_IDS: self.parser.filter_countries_ids,
            KEY_FILTER_KEYS: self.parser.filter_keys,
            KEY_ORDER: self.parser.order,
            KEY_TOTAL_PAGES: self.parser.total_pages,
            KEY_PAGE: self.parser.page,
            KEY_LIMIT: self.parser.limit
        }

    @staticmethod
    def get_users():
        user_data_list = []
        users = RulesetLogGroup.objects.filter(updated__gt=0).values_list("author").distinct()
        for user_obj in users:
            user = User.objects.get(id=user_obj[0])
            user_data = UserBuilder(user).get_data()
            user_data_list.append(user_data)

        return user_data_list

    def get_environments(self):
        env_id_list = []
        env_data_list = []
        source_environment_ids = RulesetLogGroup.objects.filter(updated__gt=0,
                                                                source_environment_id__in=self.enable_environment_ids).values_list(
            "source_environment").distinct()
        target_environment_ids = RulesetLogGroup.objects.filter(updated__gt=0,
                                                                target_environment__in=self.enable_environment_ids).values_list(
            "target_environment").distinct()
        env_id_list = self.get_distinct_environment_id(env_id_list, source_environment_ids)
        env_id_list = self.get_distinct_environment_id(env_id_list, target_environment_ids)

        for env_obj in env_id_list:
            env_data = EnvironmentBuilder(id=env_obj[0]).get_data()
            env_data_list.append(env_data)

        return env_data_list

    def get_countries(self):
        country_data_list = []
        enable_country_ids = enable_environments_countries(self.user.id, self.enable_environment_ids)
        countries = RulesetLogGroup.objects.filter(log_count__gt=0, country_id__in=enable_country_ids).values_list(
            "country").distinct()
        for country_obj in countries:
            country = Country.objects.get(id=country_obj[0])
            country_data = CountryBuilder(country).get_data()
            country_data_list.append(country_data)
        return country_data_list

    @staticmethod
    def get_distinct_environment_id(env_id_list, ids):
        for env_id in ids:
            if env_id in env_id_list:
                continue
            env_id_list.append(env_id)
        return env_id_list
