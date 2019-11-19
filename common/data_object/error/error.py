from common.data_object.error.message import RULESET_NOT_FOUND_MESSAGE, PERMISSION_DENIED_MESSAGE, \
    FOLDER_NOT_EXIST_MESSAGE, NO_AVAILABLE_DATA_MESSAGE


class PermissionDeniedError(Exception):
    def __init__(self):
        super(PermissionDeniedError, self).__init__(PERMISSION_DENIED_MESSAGE)


class NoAvailableDataError(Exception):
    def __init__(self):
        super(NoAvailableDataError, self).__init__(NO_AVAILABLE_DATA_MESSAGE)


class B2BRulesetNotFoundError(Exception):
    def __init__(self):
        super(B2BRulesetNotFoundError, self).__init__(RULESET_NOT_FOUND_MESSAGE)


class SharedStorageFolderNotFoundError(Exception):
    def __init__(self):
        super(SharedStorageFolderNotFoundError, self).__init__(FOLDER_NOT_EXIST_MESSAGE)


class SharedStorageFTPServerConnectFailError(Exception):
    def __init__(self):
        super(SharedStorageFTPServerConnectFailError, self).__init__(FOLDER_NOT_EXIST_MESSAGE)
