from common.data_object.json_builder.base import BaseBuilder
from RulesetComparer.properties.key import KEY_ID, KEY_NAME, KEY_TITLE


class MailContentTypeBuilder(BaseBuilder):

    def __init__(self, mail_content_type):
        self.mail_content_type = mail_content_type
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict[KEY_ID] = self.mail_content_type.id
        self.result_dict[KEY_NAME] = self.mail_content_type.name
        self.result_dict[KEY_TITLE] = self.mail_content_type.title


class MailContentTypesBuilder(BaseBuilder):

    def __init__(self, mail_content_types):
        self.mail_content_types = mail_content_types
        BaseBuilder.__init__(self)

    def __generate_data__(self):
        self.result_dict = self.parse_mail_content_types()

    def parse_mail_content_types(self):
        array = []
        for mail_content_type in self.mail_content_types:
            data = MailContentTypeBuilder(mail_content_type).get_data()
            array.append(data)
        return array
