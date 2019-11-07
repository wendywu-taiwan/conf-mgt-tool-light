SMTP = {
    # "login_username": "mailtest20181112@gmail.com",
    # "login_password": "shqkvjarskvbkigv",
    # "host": "smtp.gmail.com",
    # "host": "10.29.25.73",
    "host": "smtp-ch-anon.int.audatex.com",
    # "port": "465"
    "port": "25"
}

SEND_RULESET_COMPARE_RESULT_MAIL = {
    "sender": "no-reply@audatex.com",
    "receivers": ["wendy.wu@audatex.com", "engle6030@gmail.com"],
    "title": "Ruleset Compare Report",
    "ruleset_sync_title": "Ruleset Sync Up Report",
    "content": "this is the compare result",
}

SHARED_FOLDER_COMPARE_MAIL_SETTING = {
    "sender": "no-reply@audatex.com",
    "receivers": ["wendy.wu@audatex.com", "engle6030@gmail.com"],
    "title": "Shared Storage Compare Report",
    "content": "this is the compare result",
}

SEND_CLEAR_FILES_MAIL = {
    "sender": "no-reply@audatex.com",
    "receivers": ["wendy.wu@audatex.com"],
    "title": "Removed Expired Files Notice",
    "ruleset_sync_title": "Ruleset Sync Up Report",
    "content": "this is the compare result",
}
