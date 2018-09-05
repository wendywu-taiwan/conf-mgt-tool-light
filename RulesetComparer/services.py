from zeep import Client
from lxml import etree


from RulesetComparer.models import Environment
from RulesetComparer.requestModel.b2b.getOwnedBRERuleSetsModel import GetOwnedBRERuleSetsModel
from RulesetComparer.requestModel.b2b.exportRulesetModel import ExportRulesetModel
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.modelManager import get_single_model
from RulesetComparer.resource import apiResponse
from RulesetComparer.responseModel.downloadRulesetModel import DownloadRulesetModel
from RulesetComparer.responseModel.downloadSingleRulesetModel import DownloadSingleRulesetModel
from RulesetComparer.responseModel.responseModel import ResponseModel
from django.conf import settings


class RuleSetService(object):
    def download_rule_set(self, environment, country):

        env_obj = get_single_model(Environment, environment=environment, country=country)
        if env_obj is None:
            return ResponseModel.get_response_json(ResponseModel(None, apiResponse.STATUS_CODE_INVALID_PARAMETER))
        username = env_obj.userId
        password = env_obj.password
        server = env_obj.url

        print("call download_rule_set in service\n environment = %s , country = %s" % (environment, country))
        print(" username = %s \n password = %s \n server = %s" % (username, password, server))

        ruleset_list = []
        client = Client(settings.B2B_RULE_SET_CLIENT % server)
        parameter = GetOwnedBRERuleSetsModel(username, password, country).compose_request()
        response = client.service.getOwnedBRERuleSets(parameter)
        response_model = DownloadRulesetModel(response, ruleset_list)

        # check response error
        if response[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE] != 0:
            return response_model.get_response_json()

        # clean saved rulesets folders and create new one
        save_file_path = settings.RULESET_SAVED_PATH %(environment, country)
        fileManager.clear_folder(save_file_path)
        fileManager.create_folder(save_file_path)

        # parsing rulesets list and download ruleset
        bre_rule_list = etree.fromstring(response.payload.encode(settings.UNICODE_ENCODING))
        for rule in bre_rule_list:
            if len(rule) != 11:
                continue

            rule_set_name = rule[2][0].text
            response_json = self.download_single_rule_set(server, username, password, rule_set_name, save_file_path)
            ruleset_list.append(response_json)

        return response_model.get_response_json()

    @staticmethod
    def download_single_rule_set(server, username, password, rule_set_name, save_file_path):
        client = Client(settings.B2B_RULE_SET_CLIENT % server)
        parameter = ExportRulesetModel(username, password, rule_set_name).compose_request()

        print('======== download rule set %s ========' % rule_set_name)
        response = client.service.exportRuleset(parameter)
        response_model = DownloadSingleRulesetModel(response, rule_set_name)

        # save file to specific path
        save_file_name = settings.RULESET_SAVED_NAME % (save_file_path, rule_set_name)
        payload = response.payload[response.payload.index('<BRERuleList'):]
        fileManager.save_file(save_file_name, payload)

        return response_model.get_content_json()

    @staticmethod
    def download_rule_set_from_git(country):
        pass

    @staticmethod
    def compare_rule_set(country):
        pass
