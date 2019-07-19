from RulesetComparer.utils.timeUtil import get_current_utc_time
from RulesetComparer.models import RulesetLogGroup, RulesetAction, RulesetLog
from RulesetComparer.properties.key import *


class RulesetLogGroupObj:

    def __init__(self, parser, user, country):
        self.rs_log_group = None
        self.created_list = []
        self.updated_list = []
        self.deleted_list = []
        self.source_environment = parser.source_environment
        self.target_environment = parser.target_environment
        self.user = user
        self.country = country
        self.task = None
        self.commit_sha = None
        self.update_time = get_current_utc_time()
        self.backup_key = self.set_backup_key()

    def set_task(self, task):
        self.task = task

    def set_commit_sha(self, commit_sha):
        self.commit_sha = commit_sha

    def set_update_time(self, update_time):
        self.update_time = update_time
        self.backup_key = self.set_backup_key()

    def set_backup_key(self):
        return str(hash(self.update_time)) + str(hash(self.country)) + str(
            hash(self.source_environment)) + str(hash(self.target_environment))

    def update_log_group_log_count(self):
        self.rs_log_group.created = len(self.created_list)
        self.rs_log_group.updated = len(self.updated_list)
        self.rs_log_group.log_count = len(self.created_list) + len(self.updated_list)
        self.rs_log_group.save()

    def log_group(self):
        self.rs_log_group = RulesetLogGroup.objects.create(backup_key=self.backup_key,
                                                           update_time=self.update_time,
                                                           task=self.task,
                                                           source_environment=self.source_environment,
                                                           target_environment=self.target_environment,
                                                           author=self.user,
                                                           country=self.country,
                                                           commit_sha=self.commit_sha)

    def log(self, ruleset_name, action, status, exception=None):
        action = RulesetAction.objects.get(name=action)

        if action is None:
            return

        if status == STATUS_SUCCESS:
            status = 1
        else:
            status = 0

        rs_log = RulesetLog.objects.create(ruleset_log_group=self.rs_log_group,
                                           action=action,
                                           ruleset_name=ruleset_name,
                                           status=status,
                                           exception=exception)

        # ruleset create from source to target no need to backup
        if action.name == RULESET_CREATE:
            self.created_list.append(rs_log)
        # ruleset delete function is not implemented now
        if action.name == RULESET_UPDATE:
            self.updated_list.append(rs_log)
