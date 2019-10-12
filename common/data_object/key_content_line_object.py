from RulesetComparer.properties.key import *


class KeyContentLineObject:
    def __init__(self, index, context):
        self.index = index
        self.context = context
        self.key = None
        self.value = None
        self.empty_line = False
        self.parse_key_value()

    def parse_key_value(self):
        trim_context = self.context.strip(' \t\n\r')
        if trim_context is "" or self.context.startswith(KEY_S_HASH_TAG):
            self.empty_line = True
            return

        self.key = self.context

        if KEY_S_EQUAL in self.context:
            split_list = self.key.split(KEY_S_EQUAL)
            self.key = split_list[0].strip(" ")
            self.value = split_list[1]
        elif KEY_S_COLON in self.context:
            split_list = self.key.split(KEY_S_COLON)
            self.key = split_list[0].strip(" ")
            self.value = split_list[1]
