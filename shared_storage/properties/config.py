from ConfigManageTool import settings

DEPTH_COUNTRY_FOLDER = 0
DEPTH_MODULE_FOLDER = 1
DEPTH_MODULE_VERSION = 2
DEPTH_MODULE_DATA_ROOT = 3

COMPARE_RESULT_PATH = settings.BASE_DIR + "/shared_storage/compare_result/"
COMPARE_FILE_PATH = settings.BASE_DIR + "/shared_storage/tmp_file/"

COMPARE_TYPE_BLACK_LIST = {
    "ttf",
    "png",
    "jpg",
    "mp4",
    "gif",
    "dic"
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
