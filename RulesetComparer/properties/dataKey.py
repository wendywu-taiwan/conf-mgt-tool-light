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
ACTION_LIST = 'action_list'

# view.rule_download_page
RULE_NAME_LIST = 'rule_name_list'

# country
COUNTRY_KEY_ID = 'id'
COUNTRY_KEY_NAME = 'name'

# view.compare_rule_list_item_data
COMPARE_RULE_LIST_COUNTRY = 'country'
COMPARE_RULE_BASE_ENV = 'base_env'
COMPARE_RULE_COMPARE_ENV = 'compare_env'
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
KEY_SOURCE_ENV = "source_environment"
KEY_TARGET_ENV = "target_environment"
KEY_RULESETS_ARRAY = "rulesets_array"
KEY_TARGET_ENV_ONLY_RULESETS = "target_env_only_rulesets"
KEY_DIFFERENT_RULESETS = "different_rulesets"

# common
KEY_COUNTRY = "country"
KEY_NAME = "name"
KEY_COMPARE_HASH_KEY = "compare_hash_key"
KEY_TASK_ID = "task_id"

# environment name
INT2_NAME = "INT2"
INT1_NAME = "INT1"
PROD_NAME = "PROD"
GIT_NAME = "GIT"
