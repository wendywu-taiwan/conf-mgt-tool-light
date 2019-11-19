from ConfigManageTool import settings

DEPTH_COUNTRY_FOLDER = 0
DEPTH_MODULE_FOLDER = 1
DEPTH_MODULE_VERSION = 2
DEPTH_MODULE_DATA_ROOT = 3

COMPARE_RESULT_PATH = settings.BASE_DIR + "/shared_storage/compare_result/"
COMPARE_FILE_PATH = settings.BASE_DIR + "/shared_storage/tmp_file/"
ZIP_FILE_PATH = settings.BASE_DIR + "/shared_storage/tmp_file/zip_file"
ZIP_FILE_NAME_PATH = settings.BASE_DIR + "/shared_storage/tmp_file/zip_file/%s.zip"

COMPARE_RESULT_MAIL_PATH = settings.BASE_DIR + "/shared_storage/tmp_file/mail/"
GIT_SHARE_STORAGE_ROOT = settings.BASE_DIR + "/shared_storage/git_data/axn_op_apac/"
DIR_GIT_SHARE_STORAGE_ROOT = GIT_SHARE_STORAGE_ROOT + "master"

COMPARE_TYPE_BLACK_LIST = {
    "ttf",
    "ttc",
    "png",
    "jpg",
    "mp4",
    "gif",
    "dic",
    "pal",
    "pdf"
}

FILTER_MODULE_FOLDER_MAP = {
    "tw": [
        "audacx",
        "audamobile",
        "audawatch",
        "bre",
        "business",
        "config",
        "customerportal",
        "dictionary",
        "onepad",
        "searchtree",
        "template",
        "vin",
        "webpad",
        "webresources",
        "xsltStylesheets"
    ],
    "sg": [
        "audacx",
        "bre",
        "config",
        "searchtree",
        "template",
        "webpad",
        "webresources",
    ],
    "my": [
        "audacx",
        "bre",
        "business",
        "config",
        "onepad",
        "searchtree",
        "template",
        "vin",
        "webpad",
        "webresources",
        "xsltStylesheets"
    ],
    "kr": [
        "audacx",
        "audamobile",
        "audawatch",
        "axr",
        "bre",
        "business",
        "config",
        "dictionary",
        "fonts",
        "onepad",
        "partMapping",
        "searchtree",
        "template",
        "vin",
        "webpad",
        "webresources",
        "xsltStylesheets"
    ],
    "jp": [
        "bre",
        "config",
        "fonts",
        "partsinformation",
        "searchtree",
        "template",
        "webpad",
        "webresources",
    ],
    "id": [
        "audacx",
        "bre",
        "business",
        "config",
        "customreports",
        "dictionary",
        "onepad",
        "searchtree",
        "template",
        "vin",
        "webpad",
        "webresources",
        "xsltStylesheets"
    ],
    "hk": [
        "audacx",
        "audamobile",
        "axr",
        "bre",
        "business",
        "config",
        "dictionary",
        "searchtree",
        "template",
        "webpad",
        "webresources",
        "xsltStylesheets"
    ],
    "cn": [
        "audacx",
        "audamobile",
        "audawatch",
        "axr",
        "bre",
        "business",
        "config",
        "customerportal",
        "dictionary",
        "fonts",
        "idbc",
        "onepad",
        "partsinformation",
        "searchtree",
        "template",
        "vin",
        "webpad",
        "webresources",
        "xsltStylesheets"
    ],
    "other": [
        "audacx",
        "bre",
        "template",
        "webpad",
        "webresources",
        "xsltStylesheets"
    ]
}

LATEST_VERSION_GRAND_PARENT_FOLDER = [
    "/axr",
    "/h2sdfcheck"
]

LATEST_VERSION_PARENT_FOLDER = [
    "/audacx",
    "/audamobile",
    "/audawatch",
    "/axr/configuration",
    "/axr/translation",
    "/bre",
    "/business",
    "/config",
    "/customreports",
    "/customerportal",
    "/dictionary",
    "/fonts",
    "/idbc",
    "/partsinformation",
    "/onepad",
    "/searchtree",
    "/template",
    "/vin",
    "/webpad",
    "/webresources",
    "/xsltStylesheets",
    "/anonymize",
    "/audainsight",
    "/crctranslation",
    "/gotimedriver",
    "/h2sdfcheck/configuration",
    "/h2sdfcheck/translate",
    "/jexlscript",
    "/licenseplateformats",
    "/lis",
    "/lisdc",
    "/mrs",
    "/rci",
    "/rss",
    "/svisupport",
    "/temporaryfields",
    "/thatcham",
    "/vhcsupport"
]

FILTER_MODULE_FOLDER = [
    "audacx",
    "audamobile",
    "audawatch",
    "axr/configuration",
    "axr/translation",
    "bre",
    "business",
    "config",
    "customreports",
    "customerportal",
    "dictionary",
    "fonts",
    "idbc",
    "partsinformation",
    "onepad",
    "searchtree",
    "template",
    "vin",
    "webpad",
    "webresources",
    "xsltStylesheets"
]


def get_zip_file_folder_path():
    return ZIP_FILE_PATH


def get_zip_file_full_path(hash_key):
    return ZIP_FILE_NAME_PATH % hash_key
