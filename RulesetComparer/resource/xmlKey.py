SAXIF_PATH_KEY = 'saxif_path'
SAXIF_PATH = 'http://www.audatex.com/SAXIF'

# node in <Rule></Rule>
XML_NODE_COUNT = 11

XML_KEY_RULE = 'Rule'
XML_KEY_CONTEXT = 'Context'
XML_KEY_COUNTRY_ORGANIZATION_ID = 'CountryOrganizationId'
XML_KEY_ORGANIZATIONID = 'OrganizationId'
XML_KEY_RULETYPE = 'RuleType'
XML_KEY_RULE_KEY = 'Key'
XML_KEY_RULE_VALUE = 'Value'
XML_KEY_STATUS = 'Status'
XML_KEY_CREATEDBY = 'CreatedBy'
XML_KEY_CREATIONTIMESTAMP = 'CreationTimeStamp'
XML_KEY_LASTUPDATEDBY = 'LastUpdatedBy'
XML_KEY_LASTUPDATETIMESTAMP = 'LastUpdateTimeStamp'


XML_PATH_MAP = {SAXIF_PATH_KEY: SAXIF_PATH}


def filter_with_key(key):
    return SAXIF_PATH_KEY + ":" + key
