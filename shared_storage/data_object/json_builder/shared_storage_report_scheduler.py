from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleSharedStorageBuilder
from RulesetComparer.properties.key import KEY_DATA
from common.data_object.json_builder.environment import EnvironmentBuilder
from common.data_object.json_builder.ftp_region import FTPRegionBuilder
from common.data_object.json_builder.report_scheduler import ReportSchedulerBuilder


class SharedStorageReportSchedulerBuilder(ReportSchedulerBuilder, AdminConsoleSharedStorageBuilder):
    def __init__(self, user, scheduler):
        ReportSchedulerBuilder.__init__(self, scheduler)
        AdminConsoleSharedStorageBuilder.__init__(self, user)

    def __generate_data__(self):
        ReportSchedulerBuilder.__generate_data__(self)

    def get_report_data(self):
        self.result_dict["left_data_center"] = FTPRegionBuilder(region=self.scheduler.left_data_center).get_data()
        self.result_dict["right_data_center"] = FTPRegionBuilder(region=self.scheduler.right_data_center).get_data()
        self.result_dict["left_environment"] = EnvironmentBuilder(
            environment=self.scheduler.left_environment).get_data()
        self.result_dict["right_environment"] = EnvironmentBuilder(
            environment=self.scheduler.right_environment).get_data()
        self.result_dict["left_folder"] = self.scheduler.left_folder
        self.result_dict["right_folder"] = self.scheduler.right_folder
        return self.result_dict

    def get_data(self):
        self.result_dict = AdminConsoleSharedStorageBuilder.get_data(self)
        self.result_dict = self.get_report_data()
        return self.result_dict


class SharedStorageSchedulersBuilder(AdminConsoleSharedStorageBuilder):
    def __init__(self, user, schedulers):
        self.schedulers = schedulers
        AdminConsoleSharedStorageBuilder.__init__(self, user)

    def __generate_data__(self):
        AdminConsoleSharedStorageBuilder.__generate_data__(self)

    def get_data(self):
        array = []
        for scheduler in self.schedulers:
            data = SharedStorageReportSchedulerBuilder(self.user, scheduler).get_report_data()
            array.append(data)
        self.result_dict[KEY_DATA] = array
        return AdminConsoleSharedStorageBuilder.get_data(self)