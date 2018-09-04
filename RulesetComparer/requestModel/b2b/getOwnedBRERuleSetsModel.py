
from RulesetComparer.requestModel.b2b.b2bRequestModel import B2BRequestModel


class GetOwnedBRERuleSetsModel(B2BRequestModel):
    KEY_USER = 'loginId'
    KEY_PASSWORD = 'password'
    KEY_COUNTRY = 'ownerId'

    def __init__(self, user_id, password, country):
        B2BRequestModel.__init__(self)
        self.key_value_dict = {self.KEY_USER: user_id, self.KEY_PASSWORD: password, self.KEY_COUNTRY: country}



