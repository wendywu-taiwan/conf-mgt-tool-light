from zeep import Client
from RulesetComparer.models import Environment
from RulesetComparer.dataModel.requestModel.b2b.getOwnedBRERuleSetsModel import GetOwnedBRERuleSetsModel
from RulesetComparer.dataModel.requestModel.b2b.exportRulesetModel import ExportRulesetModel
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.modelManager import get_single_model
from RulesetComparer.resource import apiResponse
from RulesetComparer.dataModel.responseModel.downloadRulesetModel import DownloadRulesetModel
from RulesetComparer.dataModel.responseModel.downloadSingleRulesetModel import DownloadSingleRulesetModel
from RulesetComparer.dataModel.responseModel.b2bResponseModel import ResponseModel
from RulesetComparer.dataModel.xml.ruleListModel import RuleListModel
from RulesetComparer.utils.rulesetComparer import RulesetComparer
from RulesetComparer.dataModel.responseModel.rulesCompareModel import RulesCompareModel
from django.conf import settings


class RuleSetService(object):
    def download_rule_set(self, environment, country):
        ruleset_list = []
        response_model = DownloadRulesetModel(None, ruleset_list)
        env_obj = get_single_model(Environment, environment=environment, country=country)

        if env_obj is None:
            response_model.set_error_code(apiResponse.STATUS_CODE_INVALID_PARAMETER)
            return response_model

        username = env_obj.userId
        password = env_obj.password
        server = env_obj.url

        print("call download_rule_set in service\n environment = %s , country = %s" % (environment, country))
        print(" username = %s \n password = %s \n server = %s" % (username, password, server))

        # request to b2b owned BRE rule set service
        client = Client(settings.B2B_RULE_SET_CLIENT % server)
        parameter = GetOwnedBRERuleSetsModel(username, password, country).compose_request()
        response = client.service.getOwnedBRERuleSets(parameter)
        response_model.set_response_data(response)

        # check response error
        if response[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE] != 0:
            return response_model

        # clean saved rulesets folders and create new one
        save_file_path = settings.RULESET_SAVED_PATH % (environment, country)
        fileManager.clear_folder(save_file_path)
        fileManager.create_folder(save_file_path)

        # parsing rulesets list and download ruleset
        payload_data_encoding = response.payload.encode(settings.UNICODE_ENCODING)
        rule_list_model = RuleListModel(payload_data_encoding)

        for ruleset_name in rule_list_model.get_rule_key_list():
            single_rule_response_model = self.download_single_rule_set(environment, country, ruleset_name)
            ruleset_list.append(single_rule_response_model.get_content_json())

        return response_model

    @staticmethod
    def download_single_rule_set(environment, country, rule_set_name):
        # fileManager.save_file_to_local()
        env_obj = get_single_model(Environment, environment=environment, country=country)

        if env_obj is None:
            return ResponseModel(None, apiResponse.STATUS_CODE_INVALID_PARAMETER)
        username = env_obj.userId
        password = env_obj.password
        server = env_obj.url

        client = Client(settings.B2B_RULE_SET_CLIENT % server)
        parameter = ExportRulesetModel(username, password, rule_set_name).compose_request()

        print('======== download rule set %s ========' % rule_set_name)
        response = client.service.exportRuleset(parameter)
        response_model = DownloadSingleRulesetModel(response, rule_set_name)

        # save file to specific path
        save_file_path = settings.RULESET_SAVED_PATH % (environment, country)
        save_file_name = settings.RULESET_SAVED_NAME % (save_file_path, rule_set_name)
        if response_model.request_fail():
            return response_model

        payload = response.payload[response.payload.index('<BRERuleList'):]
        fileManager.save_file(save_file_name, payload)

        return response_model

    @staticmethod
    def download_rule_set_from_git(country):
        pass

    @staticmethod
    def compare_rule_set(country):
        # file_path = "RulesetComparer/rulesets/Int1/%s/" % country
        # extension = ".XML"
        # print(fileManager.load_file_in_folder(file_path, extension))

        ruleset1 = "RulesetComparer/rulesets/Int1/TW/RS_TW_DATA_ENTRY.XML"
        ruleset2 = "RulesetComparer/rulesets/Local/TW/RS_TW_DATA_ENTRY.XML"
        comparer = RulesetComparer(ruleset1, ruleset2)
        rules_compare_model = RulesCompareModel(comparer)
        return rules_compare_model
