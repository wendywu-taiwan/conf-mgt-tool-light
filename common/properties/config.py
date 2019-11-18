from ConfigManageTool import settings

# move common usage path here
PRELOAD_DATA_PATH = settings.BASE_DIR + "/permission/properties/" + settings.PRELOAD_DATA
AUTH_DATA_PATH = settings.BASE_DIR + "/permission/properties/" + settings.AUTH_DATA
CONF_DATA_PATH = settings.BASE_DIR + "/common/properties/conf/"
USER_ROLE_PERMISSION_DATA_PATH = settings.BASE_DIR + "/permission/properties/" + settings.USER_ROLE_PERMISSION_DATA
RULESET_ZIP_PATH = settings.BASE_DIR + "/RulesetComparer/rulesets/zip/"
RULESET_ZIP_FILE_PATH = settings.BASE_DIR + "/RulesetComparer/rulesets/zip/%s.zip"

RULESET_COMPARE_RESULT_PATH = settings.BASE_DIR + "/RulesetComparer/compare_result/"
RULESET_COMPARE_RESULT_FOLDER_PATH = settings.BASE_DIR + "/RulesetComparer/compare_result/%s/"
RULESET_COMPARE_RESULT_HTML = RULESET_COMPARE_RESULT_PATH + "%s.html"
RULESET_COMPARE_RESULT_JSON = RULESET_COMPARE_RESULT_PATH + "%s.json"
RULESET_COMPARE_RESULT_ZIP_RESOURCE = RULESET_COMPARE_RESULT_PATH + "%s/%s.html"
