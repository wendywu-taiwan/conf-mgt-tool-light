from RulesetComparer.dataModel.requestModel.b2b.b2bRequestModel import B2BRequestModel

class ExportRulesetModel(B2BRequestModel):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_RULE_SET_NAME = 'rulesetName'

    def __init__(self, user_id, password, ruleset_name):
        B2BRequestModel.__init__(self)
        self.key_value_dict = {self.KEY_USER: user_id, self.KEY_PASSWORD: password, self.KEY_RULE_SET_NAME: ruleset_name}
