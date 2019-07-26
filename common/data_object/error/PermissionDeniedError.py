class PermissionDeniedError(Exception):
    def __init__(self, message):
        super(PermissionDeniedError, self).__init__(message)
