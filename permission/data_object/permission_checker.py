from abc import abstractmethod
from permission.utils.permission_manager import *


class PermissionChecker:
    def __init__(self):
        try:
            self.is_visible = False
            self.is_editable = False
            self.check_permission()
        except BaseException as e:
            raise e

    @abstractmethod
    def check_permission(self):
        pass


class RulesetReportPermissionChecker(PermissionChecker):
    def __init__(self, user, country_id_list, base_env_id, compare_env_id):
        self.user = user
        self.country_id_list = country_id_list
        self.base_env_id = base_env_id
        self.compare_env_id = compare_env_id
        PermissionChecker.__init__(self)

    def check_permission(self):
        function_id = Function.objects.get(name=KEY_F_REPORT_TASK, module__name=KEY_M_RULESET).id

        for country_id in self.country_id_list:
            is_base_editable = is_editable(self.user.id, self.base_env_id, country_id, function_id)
            is_target_editable = is_editable(self.user.id, self.compare_env_id, country_id, function_id)

            if is_base_editable is False or is_target_editable is False:
                raise PermissionDeniedError()


class SharedStorageReportPermissionChecker(PermissionChecker):
    def __init__(self, user):
        self.user = user
        PermissionChecker.__init__(self)

    def check_permission(self):
        function_id = Function.objects.get(name=KEY_F_REPORT_TASK, module__name=KEY_M_SHARED_STORAGE).id
        function_editable = check_function_editable(self.user.id, function_id)
        if function_editable is False:
            raise PermissionDeniedError()
