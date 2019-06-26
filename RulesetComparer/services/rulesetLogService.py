from RulesetComparer.dataModel.dataParser.getRulesetLogListParser import GetRulesetLogListParser
from RulesetComparer.models import RulesetLogGroup, RulesetLog
from RulesetComparer.dataModel.dataBuilder.rulesetLogBuilder import RulesetLogBuilder
from RulesetComparer.dataModel.dataBuilder.rulesetLogListResultBuilder import RulesetLogListResultBuilder


def get_ruleset_log_list(json_data):
    parser = GetRulesetLogListParser(json_data)

    log_groups = RulesetLogGroup.objects.filter(parser.log_group_query).values().order_by('-update_time')
    parser.add_log_group_ids_query(log_groups)

    last_item_index = parser.page * parser.limit
    first_item_index = last_item_index - parser.limit

    if parser.order_descend:
        logs = RulesetLog.objects.filter(parser.log_query).values().order_by(
            '-ruleset_log_group__update_time', '-id')[first_item_index:last_item_index]
    else:
        logs = RulesetLog.objects.filter(parser.log_query).values().order_by(
            'ruleset_log_group__update_time')[first_item_index:last_item_index]

    logs_list = []
    for log in logs:
        log_obj = RulesetLogBuilder(log).get_data()
        logs_list.append(log_obj)

    data = RulesetLogListResultBuilder(parser, logs_list).get_data()
    print("result_data:" + str(data))
    return data
