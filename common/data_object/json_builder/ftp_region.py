from common.data_object.json_builder.base import BaseBuilder
from permission.models import FTPRegion
from RulesetComparer.properties.config import *


class FTPRegionBuilder(BaseBuilder):

    def __init__(self, id=None, region=None):
        try:
            if id is None:
                self.region = region
            else:
                self.region = FTPRegion.objects.get(id=id)
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.region.id
        self.result_dict[KEY_NAME] = self.region.name


class FTPRegionsBuilder(BaseBuilder):

    def __init__(self, ids=None, regions=None):
        try:
            self.regions = []
            if ids is None:
                self.regions = regions
            else:
                for id in ids:
                    self.regions.append(FTPRegion.objects.get(id=id))
            BaseBuilder.__init__(self)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict = self.parse_regions()

    def parse_regions(self):
        array = []
        for region in self.regions:
            data = FTPRegionBuilder(region=region).get_data()
            array.append(data)
        return array
