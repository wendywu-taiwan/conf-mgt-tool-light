from RulesetComparer.date_model.json_parser.get_ruleset_log_list import GetRulesetLogListParser
from RulesetComparer.date_model.json_builder.ruleset_log_list_result import RulesetLogListResultBuilder
from RulesetComparer.date_model.json_builder.ruleset_log import RulesetLogBuilder
from RulesetComparer.date_model.json_parser.show_ruleset_xml import ShowRulesetXMLParser
from RulesetComparer.models import RulesetLog


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


def get_ruleset_log_detail(detail_id):
    log = RulesetLog.objects.get_ruleset_log(detail_id)
    data = RulesetLogBuilder(log).get_data()
    return data


def get_ruleset(json_data):
    parser = ShowRulesetXMLParser(json_data)
    return parser.ruleset_array
