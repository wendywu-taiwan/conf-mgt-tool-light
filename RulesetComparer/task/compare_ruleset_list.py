import traceback

from django.template.loader import get_template

from RulesetComparer.task.download_ruleset_list import DownloadRuleListTask
from RulesetComparer.task.download_rulesets import DownloadRulesetsTask
from RulesetComparer.date_model.json_builder.ruleset_list_item import RuleListItemBuilder
from RulesetComparer.models import Country, Environment
from RulesetComparer.properties import config
from RulesetComparer.properties import key as key
from RulesetComparer.serializers.serializers import CountrySerializer, EnvironmentSerializer
from RulesetComparer.utils import fileManager, rulesetUtil
from RulesetComparer.utils.gitManager import GitManager
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.ruleListComparer import RuleListComparer
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.stringFilter import strip_list_string
from RulesetComparer.utils.timeUtil import get_current_time


class CompareRuleListTask:
    LOG_CLASS = "CompareRuleListTask"

    def __init__(self, base_env_id, compare_env_id, country_id, filter_list=None):
        self.compare_hash_key = hash(self)
        self.baseEnv = Environment.objects.get(id=base_env_id)
        self.comparedEnv = Environment.objects.get(id=compare_env_id)
        self.country = Country.objects.get(id=country_id)
        if filter_list is None:
            self.filter_list = list()
        else:
            self.filter_list = filter_list
            self.filter_list = strip_list_string(filter_list, "\\")

        self.compare_env_only_rulesets = list()
        self.base_env_only_rulesets = list()
        self.different_rulesets = list()
        self.normal_rulesets = list()

        self.compare_env_only_rules_count = 0
        self.base_env_only_rules_count = 0
        self.different_rules_count = 0

        # list rule detail data list in ruleset object
        # key = ruleset name
        # value = rule list
        self.ruleset_detail_map = {}

        # list rule diff data list in ruleset object
        # key = ruleset  name
        # value = rule diff list
        self.ruleset_diff_map = {}

        # check if environment is git
        self.git_environment = self.check_environment()
        try:
            info_log(self.LOG_CLASS, " ============== start ==============")
            info_log(self.LOG_CLASS, "env one : " + self.baseEnv.name + ", env two : " + self.comparedEnv.name)
            info_log(self.LOG_CLASS,
                     "country : " + str(self.country.name) + ", compare key:" + str(self.compare_hash_key))
            self.check_git_status()
            self.execute()
            self.save_result_file()
        except Exception as e:
            raise e

    def check_environment(self):
        if self.baseEnv.name == config.GIT.get("environment_name"):
            return key.BASE_ENVIRONMENT_GIT
        elif self.comparedEnv.name == config.GIT.get("environment_name"):
            return key.COMPARE_ENVIRONMENT_GIT
        else:
            return key.NO_ENVIRONMENT_GIT

    def check_git_status(self):
        if self.git_environment == key.NO_ENVIRONMENT_GIT:
            return

        path = get_rule_set_git_path("")
        manager = GitManager(path, settings.GIT_BRANCH_DEVELOP)
        if manager.status == GitManager.STATUS_NEED_PULL:
            manager.pull()

    def execute(self):
        if self.git_environment == key.BASE_ENVIRONMENT_GIT:
            base_rule_list = self.updated_rule_list_from_git()
            compare_rule_list = self.updated_rule_list_from_server(self.comparedEnv)
        elif self.git_environment == key.COMPARE_ENVIRONMENT_GIT:
            base_rule_list = self.updated_rule_list_from_server(self.baseEnv)
            compare_rule_list = self.updated_rule_list_from_git()
        else:
            base_rule_list = self.updated_rule_list_from_server(self.baseEnv)
            compare_rule_list = self.updated_rule_list_from_server(self.comparedEnv)

        comparer = RuleListComparer(base_rule_list, compare_rule_list)
        self.parse_compare_env_only_rulesets(comparer.comparedEnvOnly)
        self.parse_base_env_only_rulesets(comparer.baseEnvOnly)
        self.parse_union_rulesets(comparer.union)

    def updated_rule_list_from_server(self, environment):
        updated_list = DownloadRuleListTask(environment.id, self.country.id).get_result_data()
        updated_list = self.filter_ruleset_list(updated_list)
        self.download_rules(environment, updated_list)
        return updated_list

    def updated_rule_list_from_git(self):
        git_file_path = get_rule_set_git_path(self.country.name)
        updated_list = fileManager.get_rule_name_list(git_file_path)
        return self.filter_ruleset_list(updated_list)

    def filter_ruleset_list(self, ruleset_list):
        new_list = list(set(ruleset_list) - set(self.filter_list))
        return new_list

    def download_rules(self, env, rule_list):
        DownloadRulesetsTask(env.id, self.country.id, rule_list, self.compare_hash_key)

    def parse_compare_env_only_rulesets(self, rulesets):
        for ruleset_name in rulesets:
            ruleset_object = rulesetUtil.load_ruleset_object(ruleset_name, self.country.name,
                                                             self.comparedEnv.name, self.compare_hash_key)
            if ruleset_object is None:
                continue

            rule_list_item_parser = RuleListItemBuilder(ruleset_object, self.compare_hash_key)
            rule_list_item_parser.set_add_rule()
            self.compare_env_only_rulesets.append(rule_list_item_parser.get_data())
            self.ruleset_detail_map[ruleset_name] = ruleset_object.get_rules_data_array()
            self.compare_env_only_rules_count += ruleset_object.get_rules_count()

    def parse_base_env_only_rulesets(self, rulesets):
        for ruleset_name in rulesets:
            ruleset_object = rulesetUtil.load_ruleset_object(ruleset_name, self.country.name,
                                                             self.baseEnv.name, self.compare_hash_key)

            if ruleset_object is None:
                continue

            rule_list_item_parser = RuleListItemBuilder(ruleset_object, self.compare_hash_key)
            rule_list_item_parser.set_remove_rule()
            self.base_env_only_rulesets.append(rule_list_item_parser.get_data())
            self.ruleset_detail_map[ruleset_name] = ruleset_object.get_rules_data_array()
            self.base_env_only_rules_count += ruleset_object.get_rules_count()

    def parse_union_rulesets(self, rulesets):
        for ruleset_name in rulesets:
            base_ruleset_object = rulesetUtil.load_ruleset_object(ruleset_name, self.country.name,
                                                                  self.baseEnv.name, self.compare_hash_key)
            compare_ruleset_object = rulesetUtil.load_ruleset_object(ruleset_name, self.country.name,
                                                                     self.comparedEnv.name, self.compare_hash_key)

            if base_ruleset_object is None or compare_ruleset_object is None:
                continue

            comparer = RulesetComparer(ruleset_name, base_ruleset_object, compare_ruleset_object, is_module=True)
            rule_list_item_parser = RuleListItemBuilder(base_ruleset_object, self.compare_hash_key)
            if comparer.no_difference():
                rule_list_item_parser.set_normal_rule()
                self.normal_rulesets.append(rule_list_item_parser.get_data())
                self.ruleset_detail_map[ruleset_name] = base_ruleset_object.get_rules_data_array()
            else:
                rule_list_item_parser.set_modify_rule(base_ruleset_object.get_rules_count(),
                                                      compare_ruleset_object.get_rules_count(),
                                                      comparer.get_target_only_count(),
                                                      comparer.get_source_only_count(),
                                                      comparer.get_difference_count())
                self.different_rulesets.append(rule_list_item_parser.get_data())
                self.ruleset_diff_map[ruleset_name] = comparer.get_diff_data()
                self.compare_env_only_rules_count += comparer.get_target_only_count()
                self.base_env_only_rules_count += comparer.get_source_only_count()
                self.different_rules_count += comparer.get_difference_count()

    def save_result_file(self):
        current_time = get_current_time()
        base_env_data = EnvironmentSerializer(Environment.objects.get(id=self.baseEnv.id)).data
        compare_env_data = EnvironmentSerializer(Environment.objects.get(id=self.comparedEnv.id)).data
        country_data = CountrySerializer(Country.objects.get(id=self.country.id)).data
        if self.base_env_only_rules_count == 0 and self.compare_env_only_rules_count == 0 and self.different_rules_count == 0:
            has_changes = False
        else:
            has_changes = True

        compare_list_data = {
            key.COMPARE_RULE_COMPARE_HASH_KEY: self.compare_hash_key,
            key.COMPARE_RESULT_DATE_TIME: current_time,
            key.COMPARE_RESULT_ADD_LIST: self.compare_env_only_rulesets,
            key.COMPARE_RESULT_REMOVE_LIST: self.base_env_only_rulesets,
            key.COMPARE_RESULT_NORMAL_LIST: self.normal_rulesets,
            key.COMPARE_RESULT_MODIFY_LIST: self.different_rulesets,
            key.COMPARE_RESULT_ADD_FILE_COUNT: len(self.compare_env_only_rulesets),
            key.COMPARE_RESULT_REMOVE_FILE_COUNT: len(self.base_env_only_rulesets),
            key.COMPARE_RESULT_MODIFY_FILE_COUNT: len(self.different_rulesets),
            key.COMPARE_RESULT_ADD_RULE_COUNT: self.compare_env_only_rules_count,
            key.COMPARE_RESULT_REMOVE_RULE_COUNT: self.base_env_only_rules_count,
            key.COMPARE_RESULT_MODIFY_RULE_COUNT: self.different_rules_count,
            key.COMPARE_RESULT_HAS_CHANGES: has_changes

        }

        compare_result_data = {
            key.KEY_COUNTRY: country_data,
            key.KEY_BASE_ENV: base_env_data,
            key.KEY_COMPARE_ENV: compare_env_data,
            key.COMPARE_RESULT_LIST_DATA: compare_list_data,
            key.COMPARE_RESULT_DETAIL_DATA: self.ruleset_detail_map,
            key.COMPARE_RESULT_DIFF_DATA: self.ruleset_diff_map
        }

        fileManager.save_compare_result_file(self.compare_hash_key, compare_result_data)
        template = get_template("compare_result_report.html")
        html = template.render(compare_result_data)
        fileManager.save_compare_result_html(self.compare_hash_key, html)
        info_log(self.LOG_CLASS, " ============== finish ==============")

    def get_report(self):
        return fileManager.load_compare_result_file(self.compare_hash_key)
