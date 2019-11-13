from django.core.management.base import BaseCommand, CommandError
from common.properties.config import CONF_DATA_PATH
from shutil import copyfile


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('region', nargs='+', type=str)

    def handle(self, *args, **options):
        file_name = options.get("region")[0]
        conf_path = CONF_DATA_PATH
        file_path = conf_path + file_name + '_conf.py'
        copied_full_path = conf_path + "conf.py"
        copyfile(file_path, copied_full_path)
