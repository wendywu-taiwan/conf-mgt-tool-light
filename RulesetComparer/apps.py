import os, sys
from django.apps import AppConfig
from RulesetComparer.utils.logger import *


class RulesetcomparerConfig(AppConfig):
    name = 'RulesetComparer'

    def ready(self):
        # django will run twice when run server
        if os.environ.get('RUN_MAIN', None) == 'true':
            return

        if 'runserver' in sys.argv:
            from common.services.init_data import init_data
            init_data()
            from common.services.migrate_data import clear_data
            clear_data()
            from RulesetComparer.services.services import restart_all_scheduler
            restart_all_scheduler()
