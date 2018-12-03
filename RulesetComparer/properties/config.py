from django.conf import settings

FILE_PATH = {
    "rule_set_environment": "RulesetComparer/rulesets/%s/%s/%s",
    "rule_set_git": "RulesetComparer/rulesets/Git/%s",
    "compare_result": "/RulesetComparer/compare_result",
    "preload_data": "/static/preload_data.json",
    "server_log": "/RulesetComparer/serverlog"
}
FILE_NAME = {
    "_html": "%s.html",
    "_json": "%s.json",
    "_xml": "%s.xml"
}

GIT = {
    "environment_name": "GIT",
    "remote_name": "origin",
    "master_branch": "master",
    "develop_branch": "develop"
}

TIME_FORMAT = {
    "db_time_format": '%Y-%m-%d %H:%M:%S',
    "year_month_date_hour_minute_second": '%Y/%m/%d %H:%M:%S',
    "git_time_format": '%Y-%m-%d %H:%M:%S',
    "year_month_date": '%Y/%m/%d',
    "hour_minute_second": '%H:%M:%S'
}

TIME_ZONE = {
    "asia_taipei": "Asia/Taipei",
}

SMTP = {
    "login_username": "mailtest20181112@gmail.com",
    "login_password": "shqkvjarskvbkigv",
    # "login_username": "7759563f9cf606",
    # "login_password": "878057bb65bedc",
    "host": "smtp.gmail.com",
    # "host": "10.29.25.73",
    # "host": "smtp.mailtrap.io",
    "port": "465"
    # "port": "25"
}

SEND_COMPARE_RESULT_MAIL = {
    "sender": "no-reply@audatex.com",
    "receivers": ["wendy.wu@audatex.com", "engle6030@gmail.com"],
    "title": "Ruleset Compare Report",
    "content": "this is the compare result",
}

DEFAULT_LOG_TYPE = 0

LOG_TYPE_FILE = {
    0: "debug.log",
    1: "info.log",
    2: "error.log"
}


def get_rule_set_path(environment, country, compare_key):
    return FILE_PATH.get("rule_set_environment") % (compare_key, environment, country)


def get_rule_set_git_path(country):
    return FILE_PATH.get("rule_set_git") % country


def get_file_path(path_key):
    return FILE_PATH.get(path_key)


def get_file_name(file_key, compare_key):
    return FILE_NAME.get(file_key) % compare_key


def get_full_file_name(path_key, file_key, compare_key):
    return settings.BASE_DIR + "%s/%s" % (get_file_path(path_key),
                                          get_file_name(file_key, compare_key))


def get_compare_result_full_file_name(file_key, compare_key):
    return get_full_file_name("compare_result", file_key, compare_key)


def get_rule_set_full_file_name(file_path, file_name):
    return "%s/%s.xml" % (file_path, file_name)
