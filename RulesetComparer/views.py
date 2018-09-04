from RulesetComparer.services import RuleSetService


def download_rule_set(request, environment, country):
    return RuleSetService.download_rule_set(environment, country)

