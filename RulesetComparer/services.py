from zeep import Client
from lxml import etree

from RulesetComparer.models import Environment
from RulesetComparer.requestModel.b2b.getOwnedBRERuleSetsModel import GetOwnedBRERuleSetsModel
from RulesetComparer.requestModel.b2b.exportRulesetModel import ExportRulesetModel
from RulesetComparer.utils import fileManager
from RulesetComparer.utils.modelManager import get_single_model
from RulesetComparer.resource import serviceUrl as url
from RulesetComparer.resource import apiResponse
from RulesetComparer.responseModel.downloadRulesetModel import DownloadRulesetModel
from RulesetComparer.responseModel.responseModel import ResponseModel
from django.conf import settings


ruleSetSavePath = "RulesetComparer/rulesets/"


class RuleSetService(object):
    @staticmethod
    def download_rule_set(environment, country):
        ruleset_list = []
        env_obj = get_single_model(Environment, environment=environment, country=country)

        if env_obj is None:
            return ResponseModel.get_error_response_json(ResponseModel(""),
                                                         apiResponse.STATUS_CODE_INVALID_PARAMETER,
                                                         apiResponse.MESSAGE_INVALID_PARAMETER)

        username = env_obj.userId
        password = env_obj.password
        server = env_obj.url

        print("call download_rule_set in service\n environment = %s , country = %s" % (environment, country))
        print(" username = %s \n password = %s \n server = %s" % (username, password, server))

        client = Client(url.B2B_RULE_SET_CLIENT % server)
        parameter = GetOwnedBRERuleSetsModel(username, password, country).compose_request()
        response = client.service.getOwnedBRERuleSets(parameter)
        response_model = DownloadRulesetModel(response, ruleset_list)

        # check response error
        if response[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE] != 0:
            return response_model.get_response_json()

        # clean save rulesets folders
        save_file_path = ruleSetSavePath + environment + "/" + country
        fileManager.clear_folder(save_file_path)

        # parsing rulesets list and download ruleset
        bre_rule_list = etree.fromstring(response.payload.encode(settings.UNICODE_ENCODING))
        for Rule in bre_rule_list:
            if len(Rule) != 11:
                continue
            rule_set_name = Rule[2][0].text
            print('======== %s ========' % rule_set_name)
            ruleset_list.append(rule_set_name)

            parameter = ExportRulesetModel(username, password, rule_set_name).compose_request()
            response = client.service.exportRuleset(parameter)

            if response[apiResponse.B2B_RESPONSE_KEY_RETURN_CODE] != 0:
                return response_model.get_response_json()

            fileManager.create_folder(save_file_path)
            save_file_name = save_file_path + "/" + rule_set_name+'.XML'

            payload = response.payload[response.payload.index('<BRERuleList'):]
            fileManager.save_file(save_file_name, payload)

        return response_model.get_response_json()
