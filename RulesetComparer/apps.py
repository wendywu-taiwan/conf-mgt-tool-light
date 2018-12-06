from django.apps import AppConfig
from RulesetComparer.utils.logger import *


class RulesetcomparerConfig(AppConfig):
    name = 'RulesetComparer'

    def ready(self):
        initialize_logger()
        from RulesetComparer.services import initDataService
        initDataService.init_data()
