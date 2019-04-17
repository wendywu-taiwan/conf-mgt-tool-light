from django.conf import settings
from RulesetComparer.properties.dataKey import *

FILE_PATH = {
    "rule_set_environment": "RulesetComparer/rulesets/%s/%s/%s",
    "rule_set_path": "RulesetComparer/rulesets",
    "rule_set_git": "RulesetComparer/rulesets/Git/%s",
    "compare_result": "/RulesetComparer/compare_result",
    "preload_data": "/RulesetComparer/properties/jsondata/preload_data.json",
    "auth_data": "/RulesetComparer/properties/jsondata/auth_data.json",
    "server_log": "/RulesetComparer/serverlog",
    "rule_set_zip_file_name": "RulesetComparer/rulesets/zip/%s.zip",
    "rule_set_zip_file_path": "RulesetComparer/rulesets/zip",
    "rule_set_backup_path": "RulesetComparer/rulesets/backup/%s/%s/%s",
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
    "time_format_without_slash": '%Y%m%d%H%M%S',
    "year_month_date_hour_minute_second_float": '%Y/%m/%d %H:%M:%S.%f',
    "year_month_date_hour_minute_second": '%Y/%m/%d %H:%M:%S',
    "git_time_format": '%Y-%m-%d %H:%M:%S',
    "year_month_date": '%Y/%m/%d',
    "year_month_date_without_slash": '%Y%m%d',
    "hour_minute_second": '%H:%M:%S',
    "hour_minute_second_without_slash": '%H%M%S',
}

TIME_ZONE = {
    "asia_taipei": "Asia/Taipei",
}

SMTP = {
    # "login_username": "mailtest20181112@gmail.com",
    # "login_password": "shqkvjarskvbkigv",
    # "host": "smtp.gmail.com",
    "host": "10.29.25.73",
    # "port": "465"
    "port": "25"
}

SEND_COMPARE_RESULT_MAIL = {
    "sender": "no-reply@audatex.com",
    "receivers": ["wendy.wu@audatex.com", "engle6030@gmail.com"],
    "title": "Ruleset Compare Report",
    "ruleset_sync_title": "Ruleset Sync Up Report",
    "content": "this is the compare result",
}

DEFAULT_LOG_TYPE = 0
DEFAULT_MODULE_NAME = "Ruleset"

LOG_TYPE_FILE = {
    0: "info.log",
    1: "warning.log",
    2: "error.log"
}

MAIL_CONTENT_TYPE = {
    "ruleset_count_table": "ruleset_count_table",
    "ruleset_name_list": "ruleset_name_list"
}

RULESET_SYNC_UP_ACTION = [RULESET_CREATE, RULESET_UPDATE, RULESET_DELETE]


def get_rule_set_path(env_name, country_name, compare_key):
    return FILE_PATH.get("rule_set_environment") % (compare_key, env_name, country_name)


def get_ruleset_backup_path(environment, country, date):
    return FILE_PATH.get("rule_set_backup_path") % (environment, country, date)


def get_ruleset_git_root_path():
    return get_rule_set_git_path("")


def get_rule_set_git_path(country):
    return FILE_PATH.get("rule_set_git") % country


def get_file_path(path_key):
    return FILE_PATH.get(path_key)


def get_file_name(suffix, file_name):
    return FILE_NAME.get(suffix) % file_name


def get_full_file_name(path_key, file_key, compare_key):
    return settings.BASE_DIR + "%s/%s" % (get_file_path(path_key),
                                          get_file_name(file_key, compare_key))


def get_compare_result_full_file_name(file_key, compare_key):
    return get_full_file_name("compare_result", file_key, compare_key)


def get_rule_set_full_file_name(file_path, file_name):
    return "%s/%s.xml" % (file_path, file_name)


def get_rule_set_zip_file_name(compare_key):
    return FILE_PATH.get("rule_set_zip_file_name") % compare_key
