from RulesetComparer.dataModel.dataParser.getRulesetLogListParser import GetRulesetLogListParser
from RulesetComparer.dataModel.dataBuilder.rulesetLogBuilder import RulesetLogBuilder
from RulesetComparer.dataModel.dataBuilder.rulesetLogListResultBuilder import RulesetLogListResultBuilder


def get_ruleset_log_list(json_data, new_filter):
    parser = GetRulesetLogListParser(json_data, new_filter)
    logs = parser.get_logs_query_result()
    log_query = logs.query
    print("logs query:" + str(log_query))
    logs_list = []
    for log in logs:
        log_obj = RulesetLogBuilder(log).get_data()
        logs_list.append(log_obj)

    data = RulesetLogListResultBuilder(parser, logs_list).get_data()
    print("result_data:" + str(data))
    return data
