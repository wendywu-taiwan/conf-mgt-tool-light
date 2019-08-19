from abc import abstractmethod


class PermissionParser:
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
