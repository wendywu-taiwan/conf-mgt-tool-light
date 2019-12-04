from RulesetComparer.date_model.json_builder.admin_console_base import AdminConsoleRulesetBuilder
from RulesetComparer.utils.timeUtil import get_frontend_format_time
from RulesetComparer.models import RulesetLogGroup, RulesetAction
from RulesetComparer.date_model.json_builder.ruleset_log_group import RulesetLogGroupBuilder
from RulesetComparer.date_model.json_builder.ruleset_action import RulesetActionBuilder
from permission.utils.permission_manager import *


class RulesetLogBuilder(AdminConsoleRulesetBuilder):
    AUTHOR_TASK_MANAGER = "Task Manager"

    def __init__(self, user, data):
        try:
            self.user = user
            self.data = data
            self.ruleset_log_group_id = data.get(KEY_RULESET_LOG_GROUP_ID)
            self.ruleset_log_group = RulesetLogGroup.objects.filter(id=self.ruleset_log_group_id).values()[0]
            self.ruleset_log_obj = RulesetLogGroupBuilder(self.ruleset_log_group).get_data()
            self.action_id = data.get(KEY_ACTION_ID)
            self.action = RulesetAction.objects.get(id=self.action_id)
            self.ruleset_name = data.get(KEY_RULESET_NAME)
            self.status = data.get(KEY_STATUS)
            self.exception = data.get(KEY_EXCEPTION)
            self.update_time = get_frontend_format_time(self.data.get(KEY_UPDATE_TIME))
            self.backup_key = self.data.get(KEY_BACKUP_KEY)
            AdminConsoleRulesetBuilder.__init__(self, user)
        except Exception as e:
            raise e

    def __generate_data__(self):
        self.result_dict[KEY_LOG_ID] = self.data.get(KEY_ID)
        self.result_dict[KEY_BACKUP_KEY] = self.ruleset_log_obj.get(KEY_BACKUP_KEY)
        self.result_dict[KEY_UPDATE_TIME] = self.ruleset_log_obj.get(KEY_UPDATE_TIME)
        self.result_dict[KEY_USER_NAME] = self.ruleset_log_obj.get(KEY_USER_NAME)
        self.result_dict[KEY_ACTION] = RulesetActionBuilder(self.action).get_data()
        self.result_dict[KEY_SOURCE_ENV] = self.ruleset_log_obj.get(KEY_SOURCE_ENV)
        self.result_dict[KEY_TARGET_ENV] = self.ruleset_log_obj.get(KEY_TARGET_ENV)
        self.result_dict[KEY_COUNTRY] = self.ruleset_log_obj.get(KEY_COUNTRY)
        self.result_dict[KEY_RULESET_NAME] = self.ruleset_name
        self.result_dict[KEY_COMMIT_SHA] = self.parse_none(self.ruleset_log_obj.get(KEY_COMMIT_SHA))
        self.result_dict[KEY_STATUS] = self.parse_status()
        self.result_dict[KEY_EXCEPTION] = self.parse_none(self.exception)

    def parse_action(self):
        action = RulesetAction.objects.get(self.action_id)
        return action.capital_name

    def parse_status(self):
        if self.status == 1:
            return STATUS_SUCCESS
        else:
            return STATUS_FAILED
