class B2BRequestModel:

    def __init__(self):
        self.key_value_dict = {}

    def compose_request(self):
        parameter = []
        if len(self.key_value_dict) == 0:
            return parameter

        for key, value in self.key_value_dict.items():
            parameter.append(self.compose_key_value(key, value))

        return parameter

    @staticmethod
    def compose_key_value(key, value):
        return {'name': key, 'value': value}
