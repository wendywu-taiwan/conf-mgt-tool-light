GIT_NO_REPO_MSG = "git has no repository"
GIT_NO_REMOTE_REPOSITORY = "git has no remote repository"

# api response
RULESET_NOT_FOUND_MESSAGE = "the ruleset not exist on server"
PERMISSION_DENIED_MESSAGE = "you may not have the appropriate permissions."
FOLDER_NOT_EXIST_MESSAGE = "this folder not exist on server."
CONNECT_TO_FTP_SERVER_FAIL_MESSAGE = "can't connect to this FTP server."
NO_AVAILABLE_DATA_MESSAGE = "no available data for this function."

# System error
NO_SUCH_FILE = "No such file"


def get_sys_error_msg(e):
    return e.e.args[1]


def no_such_file(e):
    if get_sys_error_msg(e) == NO_SUCH_FILE:
        return True
    else:
        return False
