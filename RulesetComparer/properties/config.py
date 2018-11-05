from django.conf import settings

FILE_PATH = {
    "rule_set_environment": "RulesetComparer/rulesets/%s/%s/%s",
    "rule_set_git": "/RulesetComparer/rulesets/Git/%s",
    "compare_result": "/RulesetComparer/compare_result"

}
FILE_NAME = {
    "_html": "%s.html",
    "_json": "%s.json",
    "_xml": "%s.xml"
}


GIT = {
    "environment_name": "git",
    "remote_name": "origin",
    "master_branch": "master",
    "develop_branch": "develop"
}

SMTP = {
    "login_username": "7759563f9cf606",
    "login_password": "878057bb65bedc",
    "host": "10.29.25.73",
    # "host": "smtp.mailtrap.io",
    "port": "25"
}

SEND_COMPARE_RESULT_MAIL = {
    "sender": "no-reply@audatex.com",
    "receivers": ["wendy.wu@audatex.com"],
    "title": "Ruleset Compare Report",
    "content": "this is the compare result",
}


def get_rule_set_path(environment, country, compare_key):
    return FILE_PATH.get("rule_set_environment") % (environment, country, compare_key)


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
