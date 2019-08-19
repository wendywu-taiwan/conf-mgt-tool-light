from django.db.models import Q

from RulesetComparer.models import RulesetLog, RulesetLogGroup
from RulesetComparer.properties.key import *
from common.data_object.error.error import PermissionDeniedError
from common.utils.utility import *

from permission.models import UserRolePermission, RoleFunctionPermission, Function


def check_scheduler_detail_visibility(user_id, env_a_id, env_b_id, country_ids, function_key):
    function_id = Function.objects.get(name=function_key).id
    user_roles = UserRolePermission.objects.filter(user_id=user_id).values_list("role_permission_id", flat=True)

    query = Q()
    query.add(Q(role_permission__environment_id=env_a_id), Q.AND)
    query.add(Q(role_permission__country__in=country_ids), Q.AND)
    query.add(Q(function_id=function_id), Q.AND)
    query.add(Q(visible=1), Q.AND)
    a_visible_roles = RoleFunctionPermission.objects.filter(query).values_list("role_permission_id", flat=True)

    query = Q()
    query.add(Q(role_permission__environment_id=env_b_id), Q.AND)
    query.add(Q(role_permission__country__in=country_ids), Q.AND)
    query.add(Q(function_id=function_id), Q.AND)
    query.add(Q(visible=1), Q.AND)
    b_visible_roles = RoleFunctionPermission.objects.filter(query).values_list("role_permission_id", flat=True)

    if len(get_union(user_roles, a_visible_roles)) == 0 or len(get_union(user_roles, b_visible_roles)) == 0:
        raise PermissionDeniedError()


def check_ruleset_log_detail_visibility(user_id, log_id):
    function_id = Function.objects.get(name=KEY_F_RULESET_LOG).id
    user_roles = UserRolePermission.objects.filter(user_id=user_id).values_list("role_permission_id", flat=True)
    log = RulesetLog.objects.get_ruleset_log(log_id)
    ruleset_log_group = RulesetLogGroup.objects.get(id=log.get(KEY_RULESET_LOG_GROUP_ID))

    query = Q()
    query.add(Q(role_permission__environment_id=ruleset_log_group.source_environment.id), Q.AND)
    query.add(Q(role_permission__country_id=ruleset_log_group.country_id), Q.AND)
    query.add(Q(function_id=function_id), Q.AND)
    query.add(Q(visible=1), Q.AND)
    a_visible_roles = RoleFunctionPermission.objects.filter(query).values_list("role_permission_id", flat=True)

    query = Q()
    query.add(Q(role_permission__environment_id=ruleset_log_group.target_environment.id), Q.AND)
    query.add(Q(role_permission__country_id=ruleset_log_group.country_id), Q.AND)
    query.add(Q(function_id=function_id), Q.AND)
    query.add(Q(visible=1), Q.AND)
    b_visible_roles = RoleFunctionPermission.objects.filter(query).values_list("role_permission_id", flat=True)

    if len(get_union(user_roles, a_visible_roles)) == 0 or len(get_union(user_roles, b_visible_roles)) == 0:
        raise PermissionDeniedError()


