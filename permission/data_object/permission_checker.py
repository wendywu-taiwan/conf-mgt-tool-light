from abc import abstractmethod
from common.data_object.error.error import PermissionDeniedError
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


class SharedStorageReportPermissionChecker(PermissionChecker):
    def __init__(self, user_id):
        self.user_id = user_id
        PermissionChecker.__init__(self)

    def check_permission(self):
        function_id = Function.objects.get(name=KEY_F_REPORT_TASK, module__name=KEY_M_SHARED_STORAGE).id
        function_editable = check_function_editable(self.user_id, function_id)
        if function_editable is False:
            raise PermissionDeniedError()
