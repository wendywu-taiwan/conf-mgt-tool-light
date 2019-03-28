import traceback
from RulesetComparer.utils.logger import *
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.utils.rulesetUtil import *
from RulesetComparer.properties.config import GIT
from RulesetComparer.properties.dataKey import *
from RulesetComparer.b2bRequestTask.compareRuleListTask import CompareRuleListTask
from RulesetComparer.b2bRequestTask.createRulesetTask import CreateRulesetTask
from RulesetComparer.b2bRequestTask.updateRulesetTask import UpdateRulesetTask
from RulesetComparer.b2bRequestTask.clearRulesetTask import ClearRulesetTask
from RulesetComparer.dataModel.dataParser.createRulesetSyncSchedulerParser import CreateRulesetSyncSchedulerParser
from RulesetComparer.dataModel.dataBuilder.rulesetSyncPreDataBuilder import RulesetSyncPreDataBuilder
from RulesetComparer.models import RulesetSyncUpScheduler


def create_ruleset():
    try:
        ruleset_xml = load_rule_file_with_name("INT1", "TW", 279984339, "TEST_WENDY")
        environment = Environment.objects.get(name="INT1")
        country = Country.objects.get(name="TW")
        result_obj = CreateRulesetTask(environment, country, "TEST_WENDY", ruleset_xml).get_result_data()
        print("create ruleset result:" + str(result_obj))
    except Exception as e:
        raise e


def update_ruleset():
    try:
        ruleset_name = "RS_TW_BMW_DEFAULT"
        source_xml = load_git_file_with_name("TW", ruleset_name)
        target_xml = load_rule_file_with_name("INT1", "TW", -9223372036567344843, ruleset_name)
        environment = Environment.objects.get(name="INT1")
        country = Country.objects.get(name="TW")

        diff_json = RulesetComparer(ruleset_name, source_xml, target_xml, is_module=False).get_data_by_builder()
        target_only_rules_count = diff_json["target_env_only_rules"]["count"]

        if target_only_rules_count > 0:
            # clear ruleset first to remove deleted ruleset at target env
            result_obj = ClearRulesetTask(environment, country, ruleset_name).get_result_data()
            if result_obj.get("exception") is not None:
                return

        result_obj = UpdateRulesetTask(environment, country, ruleset_name, source_xml, target_xml,
                                       diff_json).get_result_data()
        print("create ruleset result:" + str(result_obj))
    except Exception as e:
        raise e


def create_scheduler(json_data):
    try:
        parser = CreateRulesetSyncSchedulerParser(json_data)
        info_model = RulesetSyncUpScheduler.objects.create_task(parser.source_environment_id,
                                                                parser.target_environment_id,
                                                                parser.module_id,
                                                                parser.country_list,
                                                                parser.action_list,
                                                                parser.receiver_list,
                                                                parser.interval_hour,
                                                                parser.utc_time,
                                                                parser.backup)
        return info_model
    except Exception as e:
        error_log(traceback.format_exc())
        raise e


def update_scheduler(json_data):
    pass


def sync_up_rulesets(parser):
    for country in parser.country_list:
        compare_report_json = CompareRuleListTask(parser.source_environment_id, parser.target_environment_id,
                                                  country.id).get_report()
        sync_up_report_json = RulesetSyncPreDataBuilder(compare_report_json).get_data()

        if sync_up_report_json is None:
            # error handle
            pass

        if parser.backup:
            backup_rulesets()

        if parser.action.create_ruleset:
            create_rulesets(country, parser, sync_up_report_json)

        if parser.action.update_ruleset:
            update_rulesets(country, parser, sync_up_report_json)

        if parser.action.delete_ruleset:
            delete_rulesets()


def backup_rulesets():
    pass


def create_rulesets(country, parser, sync_up_report_json):
    rulesets = sync_up_report_json["add_rulesets"]["rulesets_array"]
    result_list = []

    if len(rulesets) == 0:
        return

    for ruleset_name in rulesets:
        if parser.source_environment.name == GIT["environment_name"]:
            ruleset_xml = load_git_file_with_name(country.name, ruleset_name)
        else:
            ruleset_xml = load_rule_file_with_name(parser.source_environment.name, country.name,
                                                   sync_up_report_json[COMPARE_RULE_COMPARE_HASH_KEY], ruleset_name)

        result_obj = CreateRulesetTask(parser.target_environment, country, ruleset_name, ruleset_xml).get_result_data()
        result_list.append(result_obj)
    return result_list


def update_rulesets(country, parser, sync_up_report_json):
    rulesets = sync_up_report_json["update_rulesets"]["rulesets_array"]
    result_list = []

    if len(rulesets) == 0:
        return

    for ruleset_obj in rulesets:
        ruleset_name = ruleset_obj["name"]
        target_only_rules_count = ruleset_obj["target_env_only_rules"]["count"]

        if target_only_rules_count > 0:
            # clear ruleset first to remove deleted ruleset at target env
            result_obj = ClearRulesetTask(parser.target_environment, country, ruleset_name).get_result_data()

            if result_obj.get("exception") != "":
                result_list.append(result_obj)
                continue

        if parser.source_environment.name == GIT["environment_name"]:
            source_xml = load_git_file_with_name(country.name, ruleset_name)
            target_xml = load_rule_file_with_name(parser.target_environment.name, country.name,
                                                  sync_up_report_json[COMPARE_RULE_COMPARE_HASH_KEY], ruleset_name)
        elif parser.target_environment == GIT["environment_name"]:
            source_xml = load_rule_file_with_name(parser.source_environment.name, country.name,
                                                  sync_up_report_json[COMPARE_RULE_COMPARE_HASH_KEY], ruleset_name)
            target_xml = load_git_file_with_name(country.name, ruleset_name)
        else:
            source_xml = load_rule_file_with_name(parser.source_environment.name, country.name,
                                                  sync_up_report_json[COMPARE_RULE_COMPARE_HASH_KEY], ruleset_name)
            target_xml = load_rule_file_with_name(parser.target_environment.name, country.name,
                                                  sync_up_report_json[COMPARE_RULE_COMPARE_HASH_KEY], ruleset_name)

        result_obj = UpdateRulesetTask(parser.target_environment, country, ruleset_name, source_xml, target_xml,
                                       ruleset_obj).get_result_data()
        result_list.append(result_obj)
    return result_list


def delete_rulesets():
    pass


def send_mail():
    pass
