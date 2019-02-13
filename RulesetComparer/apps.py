import os, sys
from django.apps import AppConfig
from RulesetComparer.utils.logger import *
from RulesetComparer.services.services import restart_all_scheduler


class RulesetcomparerConfig(AppConfig):
    name = 'RulesetComparer'

    def ready(self):
        # django will run twice when run server
        if os.environ.get('RUN_MAIN', None) == 'true':
            return
        if 'manage.py' not in sys.argv:
            restart_all_scheduler()
