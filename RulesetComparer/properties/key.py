# RulesCompareBuilder
RULE_SET_NAME = 'name'
RULE_SET_BASE_ONLY_DATA = 'base_env_data'
RULE_SET_COMPARED_ONLY_DATA = 'compared_env_data'
RULE_SET_DIFF_DATA = 'diff_data'

# RuleListItemBuilder
RULE_LIST_ITEM_NAME = 'name'
RULE_LIST_ITEM_TABLE_TYPE = 'table_type'
RULE_LIST_ITEM_COMPARE_HASH_KEY = 'hash_key'
RULE_LIST_ITEM_BASE_COUNT = 'base_count'
RULE_LIST_ITEM_NEW_COUNT = 'new_count'
RULE_LIST_ITEM_ADD_COUNT = 'add_count'
RULE_LIST_ITEM_REMOVE_COUNT = 'remove_count'
RULE_LIST_ITEM_MODIFY_COUNT = 'modify_count'
RULE_LIST_ITEM_BASE_ENV_DATA = 'base_env_data'
RULE_LIST_ITEM_COMPARED_ENV_DATA = 'compared_env_data'
RULE_LIST_ITEM_DIFF_DATA = 'diff_data'

RULE_LIST_ITEM_TABLE_TYPE_ADD = 'add'
RULE_LIST_ITEM_TABLE_TYPE_REMOVE = 'remove'
RULE_LIST_ITEM_TABLE_TYPE_MODIFY = 'modify'
RULE_LIST_ITEM_TABLE_TYPE_NORMAL = 'normal'

# RuleSetBuilder, RuleModifiedBuilder
RULE_KEY_PROCESS = 'process'
RULE_KEY_PROCESS_STEP = 'process_step'
RULE_KEY_ORGANIZATION_ID = 'organization_id'
RULE_KEY_OWNER_RULE = 'owner_role'
RULE_KEY_RULE_TYPE = 'rule_type'
RULE_KEY_RULE_KEY = 'key'
RULE_KEY_RULE_VALUE = 'value'
RULE_KEY_RULE_EXPRESSION = 'expression'
RULE_MODIFIED_KEY_BASE_VALUE = 'base_value'
RULE_MODIFIED_KEY_BASE_EXPRESSION = 'base_expression'
RULE_MODIFIED_KEY_COMPARE_VALUE = 'compare_value'
RULE_MODIFIED_KEY_COMPARE_EXPRESSION = 'compare_expression'
RULE_KEY_COMBINED_KEY = 'combined_key'

# view.environment_select , view.admin_console_create_task, view.rule_download_page
ENVIRONMENT_SELECT_COUNTRY = 'countries'
ENVIRONMENT_SELECT_ENVIRONMENT = 'environments'
SOURCE_ENVIRONMENT = 'source_environment'
TARGET_ENVIRONMENT = 'target_environment'

# view.rule_download_page
RULE_NAME_LIST = 'rule_name_list'

# country
COUNTRY_KEY_ID = 'id'
COUNTRY_KEY_NAME = 'name'

# view.compare_rule_list_item_data
COMPARE_RULE_COMPARE_HASH_KEY = 'compare_hash_key'
COMPARE_RESULT_DATE_TIME = 'current_time'
COMPARE_RESULT_ADD_LIST = 'add_list'
COMPARE_RESULT_REMOVE_LIST = 'remove_list'
COMPARE_RESULT_NORMAL_LIST = 'normal_list'
COMPARE_RESULT_MODIFY_LIST = 'modify_list'
COMPARE_RESULT_ADD_FILE_COUNT = 'add_file_count'
COMPARE_RESULT_REMOVE_FILE_COUNT = 'remove_file_count'
COMPARE_RESULT_MODIFY_FILE_COUNT = 'modify_file_count'
COMPARE_RESULT_ADD_RULE_COUNT = 'add_rule_count'
COMPARE_RESULT_REMOVE_RULE_COUNT = 'remove_rule_count'
COMPARE_RESULT_MODIFY_RULE_COUNT = 'modify_rule_count'
COMPARE_RESULT_HAS_CHANGES = 'has_changes'
COMPARE_RESULT_LIST_DATA = 'list_data'
COMPARE_RESULT_DETAIL_DATA = 'detail_data'
COMPARE_RESULT_DIFF_DATA = 'diff_data'
COMPARE_RESULT_INFO_DATA = 'info_data'

# view.rule_detail, view.rule_diff
RULE_KEY_ENVIRONMENT_NAME = 'environment_name'
RULE_KEY_ENVIRONMENT_ID = 'environment_id'
RULE_KEY_COUNTRY_NAME = 'country_name'
RULE_KEY_COUNTRY_ID = 'country_id'
RULE_KEY_COMPARE_HASH_KEY = 'compare_hash_key'
RULE_KEY_RULE_NAME = 'rule_name'
RULE_KEY_RULE_DATA = 'rule_data'
RULE_DIFF_KEY_BASE_ENV_NAME = 'base_env_name'
RULE_DIFF_KEY_COMPARED_ENV_NAME = 'compare_env_name'
RULE_DIFF_KEY_ADD_LIST = 'add_list'
RULE_DIFF_KEY_REMOVE_LIST = 'remove_list'
RULE_DIFF_KEY_MODIFY_LIST = 'modify_list'
RULE_DIFF_KEY_NORMAL_LIST = 'normal_list'
RULE_DIFF_HAS_CHANGES = 'has_changes'

# environment model key
NO_ENVIRONMENT_GIT = 0
BASE_ENVIRONMENT_GIT = 1
COMPARE_ENVIRONMENT_GIT = 2

# task status
STATUS_ENABLE = 1
STATUS_DISABLE = 0

# response builder
SUCCESS_MESSAGE = "success"

# view.server_log
LOG_TYPE_KEY = "log_type_key"
LOG_TYPE = "log_type"
LOG_CONTENT = "log_content"

# view.admin_console_scheduler_list
SCHEDULER_LIST = "task_list"

# view.admin_console_create_scheduler
ADMIN_CONSOLE_INFO = "admin_console_info"

# view.admin_console_update_scheduler
SCHEDULER_DATA = "scheduler_data"

# B2B_SERVICE
B2B_SERVICE_RULESET_ASSIGNMENT = "ruleset_assignment"

# MAIL CONTENT TYPE
RULESET_MAIL_CONTENT_TYPE = "mail_content_types"
RULESET_COUNT_TABLE = "ruleset_count_table"
RULESET_NAME_LIST = "ruleset_name_list"

# RULESET SYNC UP ACTION
RULESET_CREATE = "create"
RULESET_UPDATE = "update"
RULESET_DELETE = "delete"
RULESET_CLEAR = "clear"

# RulesetB2BActionResultBuilder
STATUS_SUCCESS = "success"
STATUS_FAILED = "failed"

# RulesetSyncPreDataBuilder
KEY_RULESETS_ARRAY = "rulesets_array"
KEY_RULES_ARRAY = "rules_array"
KEY_SOURCE_ENV_ONLY_RULESETS = "source_env_only_rulesets"
KEY_SOURCE_ENV_ONLY_RULES = "source_env_only_rules"
KEY_TARGET_ENV_ONLY_RULESETS = "target_env_only_rulesets"
KEY_TARGET_ENV_ONLY_RULES = "target_env_only_rules"
KEY_DIFFERENT_RULESETS = "different_rulesets"
KEY_HAS_RECOVERY_RULESETS = "has_recovery_rulesets"
KEY_NORMAL_RULES = "normal_rules"
KEY_DIFFERENT_RULES = "different_rules"

# RulesetFilterBackupObjectBuilder, RecoverRulesetsResultBuilder, RulesetSyncResultDataBuilder
KEY_FOLDER_NAME = "folder_name"
KEY_BACKUP_RULESETS_LIST = "backup_rulesets_list"
KEY_CREATED_RULESETS = "created_rulesets"
KEY_UPDATED_RULESETS = "updated_rulesets"
KEY_DELETED_RULESETS = "deleted_rulesets"
KEY_APPLIED_RULESETS = "applied_rulesets"
KEY_ACTION = "action"
KEY_CREATED = "created"
KEY_UPDATED = "updated"
KEY_DELETED = "deleted"
KEY_FAILED_RULESETS = "failed_rulesets"

# recoverRulesetsParser
KEY_SELECT_FOLDER_NAME = "select_folder_name"

# RulesetSyncSchedulerBuilder
KEY_RECEIVER_LIST = "receiver_list"
KEY_BACKUP_YES = 1
KEY_BACKUP_NO = 0

# BackupDatesBuilder
KEY_RULESET_LOG_GROUP_ID = "ruleset_log_group_id"
KEY_DATES = "dates"

KEY_USER_NAME = "user_name"

# RulesetLogListResultBuilder
KEY_USERS = "users"
KEY_ENVIRONMENTS = "environments"
KEY_COUNTRIES = "countries"
KEY_FILTER_USER_IDS = "filter_user_ids"
KEY_FILTER_ENVIRONMENT_IDS = "filter_environment_ids"
KEY_FILTER_COUNTRIES_IDS = "filter_countries_ids"
KEY_FILTER_KEYS = "filter_keys"
KEY_ORDER = "order"

# common
KEY_ID = "id"
KEY_LOG_ID = "log_id"
KEY_COUNTRY = "country"
KEY_COUNTRIES = "countries"
KEY_ENVIRONMENT = "environment"
KEY_ENVIRONMENTS = "environments"
KEY_ENVIRONMENT_ID = "environment_id"
KEY_COUNTRY_ID = "country_id"
KEY_NAME = "name"
KEY_TYPE = "type"
KEY_SIZE = "size"
KEY_DEPTH = "depth"
KEY_INDEX = "index"
KEY_MODIFICATION_TIME = "modification_time"
KEY_CHILD_NODES = "child_nodes"
KEY_DIFF_RESULT = "diff_result"
KEY_CAPITAL_NAME = "capital_name"
KEY_FULL_NAME = "full_name"
KEY_COMPARE_HASH_KEY = "compare_hash_key"
KEY_TASK_ID = "task_id"
KEY_DATE_TIME = "date_time"
KEY_COMPARE_TIME = "compare_time"
KEY_COUNT = "count"
KEY_RULESETS = "rulesets"
KEY_UPDATED_TIME = "updated_time"
ACTION_LIST = 'action_list'
KEY_EXCEPTION = "exception"
KEY_BACKUP = "backup"
KEY_BACKUP_KEY = "backup_key"
KEY_BACKUP_FOLDER = "backup_folder"
KEY_ICON_FILE_NAME = "icon_file_name"
KEY_COUNTRY_LIST = "country_list"
KEY_INTERVAL_HOUR = "interval_hour"
KEY_INTERVAL = "interval"
KEY_LAST_PROCEED_TIME = "last_proceed_time"
KEY_NEXT_PROCEED_TIME = "next_proceed_time"
KEY_CREATED_TIME = "created_time"
KEY_CREATOR = "creator"
KEY_EDITOR = "editor"
KEY_ENABLE = "enable"
KEY_EMAIL = "email"
KEY_STATUS = "status"
KEY_BACKUP_DATES = "backup_dates"
KEY_UPDATE_TIME = "update_time"
KEY_BASE_ENV = 'base_env'
KEY_COMPARE_ENV = 'compare_env'
KEY_SOURCE_ENV = "source_environment"
KEY_SOURCE_ENV_ID = "source_environment_id"
KEY_TARGET_ENV = "target_environment"
KEY_TARGET_ENV_ID = "target_environment_id"
KEY_COMMIT_SHA = "commit_sha"
KEY_LOG_COUNT = "log_count"
KEY_RULESET_LOG_GROUPS = "ruleset_log_groups"
KEY_RULESET_LOGS = "ruleset_logs"
KEY_ACTION_ID = "action_id"
KEY_AUTHOR = "author"
KEY_AUTHOR_ID = "author_id"
KEY_RULESET_NAME = "ruleset_name"
KEY_PAGE = "page"
KEY_TOTAL_PAGES = "total_pages"
KEY_LIMIT = "limit"
KEY_RULESET_LOG_LIST = "ruleset_log_list"
KEY_LOG_DATA = "log_data"
KEY_RULESET_DATA = "ruleset_data"
KEY_RULESET_PATH_INFO = "ruleset_path_info"
KEY_USER_DATA = "user_data"
KEY_MODULE_DATA = "module_data"
KEY_FUNCTIONS_DATA = "functions_data"
KEY_FUNCTION = "function"
KEY_DISPLAY_NAME = "display_name"
KEY_VISIBLE = "visible"
KEY_EDITABLE = "editable"
KEY_NAVIGATION_INFO = "navigation_info"
KEY_CHECKED = "checked"
KEY_ROLE_TYPE = "role_type"
KEY_ENVIRONMENT_ROLE = "environment_role"
KEY_ROLE_PERMISSION = "role_permission"
KEY_FUNCTION_ROLE_PERMISSION = "function_role_permission"
KEY_TITLE = "title"
KEY_DATA = "data"
KEY_FREQUENCY_TYPE = "frequency_type"
KEY_FREQUENCY_TYPES = "frequency_types"
KEY_FILE_NAME = "file_name"
KEY_LEFT_FILE = "left_file"
KEY_LEFT_ENVIRONMENT = "left_environment"
KEY_RIGHT_ENVIRONMENT = "right_environment"
KEY_LEFT_REGION = "left_region"
KEY_RIGHT_REGION = "right_region"
KEY_LEFT_FOLDER = "left_folder"
KEY_RIGHT_FOLDER = "right_folder"
KEY_LEFT_DIFF_RESULT = "left_diff_result"
KEY_RIGHT_DIFF_RESULT = "right_diff_result"
KEY_RIGHT_FILE = "right_file"
KEY_CHANGED = "changed"
KEY_ADDED = "added"
KEY_BLANK = "blank"
KEY_CONTEXT = "context"
KEY_ROW = "row"
KEY_INDEX = "index"
KEY_PARENT_INDEX = "parent_index"
KEY_LEFT_TYPE = "left_type"
KEY_LEFT_ROW = "left_row"
KEY_LEFT_LINE = "left_line"
KEY_RIGHT_TYPE = "right_type"
KEY_RIGHT_ROW = "right_row"
KEY_RIGHT_LINE = "right_line"
KEY_SIDE = "side"
REQUEST_GET = 'GET'
REQUEST_POST = 'POST'

# environment name
INT2_NAME = "INT2"
INT1_NAME = "INT1"
PROD_NAME = "PROD"
GIT_NAME = "GIT"

# module_key
KEY_M_RULESET = "ruleset"
KEY_M_SETTING = "setting"

# frequency_key
KEY_DAYS = "days"
KEY_WEEKS = "weeks"

# function key
KEY_F_RECOVERY = "recovery"
KEY_F_AUTO_SYNC_TASK = "auto_sync_task"
KEY_F_REPORT_TASK = "report_task"
KEY_F_RULESET_LOG = "ruleset_log"
KEY_F_SERVER_LOG = "server_log"
KEY_F_USER_ROLE = "user_role"
KEY_F_ROLE_PERMISSION = "role_permission"

# File Type key
KEY_FOLDER = "folder"
KEY_OTHERS = "other"
KEY_XML = "xml"
KEY_PROPERTIES = "properties"
KEY_XSL = "xsl"
KEY_PNG = "png"
KEY_EXE = "exe"
KEY_JSON = "json"
KEY_CSS = "css"
KEY_XSLT = "xslt"

# Diff Result Key
KEY_D_RESULT_ADD = "add"
KEY_D_RESULT_REMOVE = "remove"
KEY_D_RESULT_SAME = "same"
KEY_D_RESULT_DIFFERENT = "different"

# symbol
KEY_S_EQUAL = "="
KEY_S_HASH_TAG = "#"
