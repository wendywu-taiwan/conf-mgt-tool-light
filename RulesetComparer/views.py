from RulesetComparer.services import RuleSetService


def download_rule_set(request, environment, country):
    return RuleSetService.download_rule_set(RuleSetService(), environment, country)


def download_rule_set_from_git(request, country):
    return RuleSetService.download_rule_set_from_git(country)


def compare_country_rule_set(request, country):
    return RuleSetService.compare_rule_set(country)
