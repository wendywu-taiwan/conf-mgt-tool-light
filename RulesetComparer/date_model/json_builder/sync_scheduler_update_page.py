from RulesetComparer.date_model.json_builder.ruleset_sync_scheduler import RulesetSyncSchedulerBuilder
from RulesetComparer.date_model.json_builder.sync_scheduler_create_page import SyncSchedulerCreatePageBuilder
from RulesetComparer.models import RulesetSyncUpScheduler
from common.data_object.json_builder.country import CountriesBuilder
from common.data_object.json_builder.environment import EnvironmentsBuilder
from common.data_object.json_builder.frequency_type import FrequencyTypesBuilder
from common.models import FrequencyType
from RulesetComparer.properties.key import *


class SyncSchedulerUpdatePageBuilder(SyncSchedulerCreatePageBuilder):

    def __init__(self, user, scheduler_id):
        self.scheduler = RulesetSyncUpScheduler.objects.get(id=scheduler_id)
        SyncSchedulerCreatePageBuilder.__init__(self, user)

    def __generate_data__(self):
        self.result_dict[SOURCE_ENVIRONMENT] = EnvironmentsBuilder(environments=[self.git_environment]).get_data()
        self.result_dict[TARGET_ENVIRONMENT] = EnvironmentsBuilder(environments=[self.int2_environment]).get_data()
        self.result_dict[ENVIRONMENT_SELECT_COUNTRY] = CountriesBuilder(countries=self.countries).get_data()
        self.result_dict[ACTION_LIST] = self.action_list
        self.result_dict[KEY_FREQUENCY_TYPES] = FrequencyTypesBuilder(FrequencyType.objects.all()).get_data()
        self.result_dict[SCHEDULER_DATA] = RulesetSyncSchedulerBuilder(None, self.scheduler).get_data()
