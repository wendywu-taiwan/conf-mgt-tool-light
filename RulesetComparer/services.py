from RulesetComparer.utils import fileManager
from RulesetComparer.apiRequestTask.b2b.downloadRuleSetTask import DownloadRuleSetTask
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.dataModel.responseModel.rulesCompareModel import RulesCompareModel
from RulesetComparer.apiRequestTask.b2b.downloadRuleListTask import DownloadRuleListTask
from RulesetComparer.utils.ruleListComparer import RuleListComparer
from RulesetComparer.dataModel.responseModel.ruleListCompareModel import RuleListCompareModel
from RulesetComparer.dataModel.xml.rulesModel import RulesModel as ParseRuleModel
from RulesetComparer.dataModel.responseModel.rulesModel import RulesModel as ResponseRulesModel
from django.conf import settings


class RuleSetService(object):

    @staticmethod
    def get_rule_list_from_b2b(environment, country):
        task = DownloadRuleListTask(environment, country)
        return task

    @staticmethod
    def get_rule_from_b2b(environment, country, rule_set_name):
        task = DownloadRuleSetTask(environment, country, rule_set_name)

        ruleset = task.get_rule_set_file()
        rules_model = ParseRuleModel(ruleset)
        response_model = ResponseRulesModel(rules_model)
        return response_model

    def compare_rule_list(self, environment1, environment2, country):
        rule_list_1 = self.get_rule_list_from_b2b(environment1, country).get_content()
        rule_list_2 = self.get_rule_list_from_b2b(environment2, country).get_content()
        comparer = RuleListComparer(rule_list_1, rule_list_2)
        response_model = RuleListCompareModel(environment1, environment2, comparer)
        return response_model




    # def download_rule_set_from_b2b(self, environment, country):
    #
    #
    #     ruleset_list = []
    #     response_model = DownloadRuleListTask(None, ruleset_list)
    #     env_obj = get_single_model(Environment, environment=environment, country=country)
    #
    #     if env_obj is None:
    #         response_model.set_error_code(apiResponse.STATUS_CODE_INVALID_PARAMETER)
    #         return response_model
    #
    #     username = env_obj.userId
    #     password = env_obj.password
    #     server = env_obj.url
    #
    #     print("call download_rule_set in service\n environment = %s , country = %s" % (environment, country))
    #     print(" username = %s \n password = %s \n server = %s" % (username, password, server))
    #
    #     # request to b2b owned BRE rule set service
    #     client = Client(settings.B2B_RULE_SET_CLIENT % server)
    #     parameter = GetOwnedBRERuleSetsModel(username, password, country).compose_request()
    #     response = client.service.getOwnedBRERuleSets(parameter)
    #     response_model.set_response_data(response)
    #
    #     # check response error
    #     if response[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE] != 0:
    #         return response_model
    #
    #     # clean saved rulesets folders and create new one
    #     save_file_path = settings.RULESET_SAVED_PATH % (environment, country)
    #     fileManager.clear_folder(save_file_path)
    #     fileManager.create_folder(save_file_path)
    #
    #     # parsing rulesets list and download ruleset
    #     payload_data_encoding = response.payload.encode(settings.UNICODE_ENCODING)
    #     rule_list_model = RuleListModel(payload_data_encoding)
    #
    #     for ruleset_name in rule_list_model.get_rules_file_name_list():
    #         single_rule_response_model = self.download_single_rule_set_from_b2b(environment, country, ruleset_name)
    #         ruleset_list.append(single_rule_response_model.get_content_json())
    #
    #     return response_model

    # @staticmethod
    # def download_single_rule_set_from_b2b(environment, country, rule_set_name):
    #     # fileManager.save_file_to_local()
    #     env_obj = get_single_model(Environment, environment=environment, country=country)
    #
    #     if env_obj is None:
    #         return ResponseModel(None, apiResponse.STATUS_CODE_INVALID_PARAMETER)
    #     username = env_obj.userId
    #     password = env_obj.password
    #     server = env_obj.url
    #
    #     client = Client(settings.B2B_RULE_SET_CLIENT % server)
    #     parameter = DownloadRuleSetTask(username, password, rule_set_name).compose_request()
    #
    #     print('======== download rule set %s ========' % rule_set_name)
    #     response = client.service.exportRuleset(parameter)
    #     response_model = DownloadSingleRulesetModel(response, rule_set_name)
    #
    #     # save file to specific path
    #     save_file_path = settings.RULESET_SAVED_PATH % (environment, country)
    #     save_file_name = settings.RULESET_SAVED_NAME % (save_file_path, rule_set_name)
    #     if response_model.request_fail():
    #         return response_model
    #
    #     payload = response.payload[response.payload.index('<BRERuleList'):]
    #     fileManager.save_file(save_file_name, payload)
    #
    #     return response_model

    @staticmethod
    def download_rule_set_from_git(country):
        pass

    @staticmethod
    def compare_rule_set(env1, env2, country, rule_set_name):
        task1 = DownloadRuleSetTask(env1, country, rule_set_name)
        task2 = DownloadRuleSetTask(env2, country, rule_set_name)

        rules_module1 = ParseRuleModel(task1.get_rule_set_file())
        rules_module2 = ParseRuleModel(task2.get_rule_set_file())

        comparer = RulesetComparer(rules_module1, rules_module2)
        response_model = RulesCompareModel(env1, env2, rule_set_name, comparer)

        return response_model
