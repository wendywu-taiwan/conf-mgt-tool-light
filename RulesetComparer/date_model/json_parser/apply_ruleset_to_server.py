from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.date_model.json_parser.base_apply_ruleset import BaseApplyRulesetParser
from RulesetComparer.date_model.json_parser.permission import PermissionParser
from permission.utils.permission_manager import *
from permission.models import Function
from RulesetComparer.properties.key import *
from common.data_object.error.error import PermissionDeniedError


class ApplyRulesetToServerParser(BaseApplyRulesetParser, PermissionParser):
    def __init__(self, json_data, user):
        try:
            self.data = json_data
            self.user = user
            BaseApplyRulesetParser.__init__(self)
            PermissionParser.__init__(self)
        except BaseException as e:
            raise e

    def parse_ruleset_data(self):
        self.source_environment = Environment.objects.get(name=BACKUP_ENVIRONMENT_NAME)

        target_environment_id = self.data.get(KEY_ENVIRONMENT_ID)
        self.target_environment = Environment.objects.get(id=target_environment_id)

        country_id = self.data.get(KEY_COUNTRY_ID)
        self.country = Country.objects.get(id=country_id)

        self.backup_key = self.data.get(KEY_BACKUP_KEY)
        self.rulesets.append(self.data.get(KEY_RULESET_NAME))

        if self.data.get(KEY_BACKUP_FOLDER) == ENVIRONMENT_SOURCE:
            self.ruleset_path = get_backup_path_applied_version(self.backup_key)
        else:
            self.ruleset_path = get_backup_path_server_version(self.backup_key)

    def check_permission(self):
        function_id = Function.objects.get(name=KEY_F_RECOVERY).id
        target_env_id = self.target_environment.id
        country_id = self.country.id

        self.is_editable = is_editable(self.user.id, target_env_id, country_id, function_id)
        if not self.is_editable:
            raise PermissionDeniedError()
