from RulesetComparer.utils.rulesetUtil import *


class RulesetDiffCompareResultParser:
    def __init__(self, compare_result_data, ruleset_name):
        try:
            self.compare_result_data = compare_result_data
            self.ruleset_name = ruleset_name
            self.source_environment_id = (compare_result_data.get(KEY_BASE_ENV)).get(KEY_ID)
            self.source_environment = Environment.objects.get(id=self.source_environment_id)
            self.target_environment_id = (compare_result_data.get(KEY_COMPARE_ENV)).get(KEY_ID)
            self.target_environment = Environment.objects.get(id=self.target_environment_id)
            self.country_id = (compare_result_data.get(KEY_COUNTRY)).get(KEY_ID)
            self.country = Country.objects.get(id=self.country_id)
            self.ruleset_diff_data = (compare_result_data.get(COMPARE_RESULT_DIFF_DATA)).get(ruleset_name)
        except Exception as e:
            raise e
