from RulesetComparer.models import B2BRuleSetServer, Country, Environment
from RulesetComparer.utils.modelManager import create_model


class InsertDataService(object):

    def init_b2b_rule_set_server_db_data(self):
        tw_country_id = Country.objects.get(name="TW").id
        local_env_id = Environment.objects.get(name="Local").id
        int1_env_id = Environment.objects.get(name="Int1").id
        int2_env_id = Environment.objects.get(name="Int2").id
        git_env_id = Environment.objects.get(name="Git").id

        init_data_list = [
            [tw_country_id, local_env_id, "inside_TWadmin", "audatex", "localhost:8181", True],
            [tw_country_id, int1_env_id, "inside_TWadmin", "audatex", "www-int1.audatex.sg", True],
            [tw_country_id, int2_env_id, "inside_TWadmin", "audatex", "www-int2.audatex.sg", False],
            [tw_country_id, git_env_id, "inside_TWadmin", "audatex", "", True]
        ]

        for data in init_data_list:
            self.create_b2b_server(data[0], data[1], data[2], data[3], data[4], data[5])

    @staticmethod
    def create_b2b_server(country_id, env_id, user_id, password, url, accessible):
        create_model(B2BRuleSetServer,
                     country_id=country_id,
                     environment_id=env_id,
                     user_id=user_id,
                     password=password,
                     url=url,
                     accessible=accessible)
