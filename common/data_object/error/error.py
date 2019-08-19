from common.data_object.error.message import RULESET_NOT_FOUND_MESSAGE, PERMISSION_DENIED_MESSAGE


class PermissionDeniedError(Exception):
    def __init__(self):
        super(PermissionDeniedError, self).__init__(PERMISSION_DENIED_MESSAGE)


class B2BRulesetNotFoundError(Exception):
    def __init__(self):
        super(B2BRulesetNotFoundError, self).__init__(RULESET_NOT_FOUND_MESSAGE)
