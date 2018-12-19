import os
from django.apps import AppConfig
from RulesetComparer.utils.logger import *


class RulesetcomparerConfig(AppConfig):
    name = 'RulesetComparer'

    def ready(self):
        # django will run twice when run server
        if os.environ.get('RUN_MAIN', None) == 'true':
            return

        initialize_logger()
