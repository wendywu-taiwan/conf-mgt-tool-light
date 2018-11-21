SAXIF_PATH_KEY = 'saxif_path'
SAXIF_PATH = 'http://www.audatex.com/SAXIF'

# node in <Rule></Rule>
XML_NODE_COUNT = 11

# XML_KEY
NODE_KEY_RULE = 'Rule'
COUNTRY_ORGANIZATION_ID = 'CountryOrganizationId'
RULE_TYPE = 'RuleType'
RULE_KEY = 'Key'
RULE_VALUE = 'Value'
STATUS = 'Status'
EXPRESSION = 'Expression'
CREATED_BY = 'CreatedBy'
CREATION_TIME_STAMP = 'CreationTimeStamp'
LAST_UPDATE_DBY = 'LastUpdatedBy'
LAST_UPDATE_TIME_STAMP = 'LastUpdateTimeStamp'


NODE_KEY_CONTEXT = 'Context'
# data in node <Context></Context>
PROCESS = 'Process'
ORGANIZATION_ID = 'OrganizationId'
OWNER_RULE = 'OwnerRole'
PROCESS_STEP = 'ProcessStep'


XML_PATH_MAP = {SAXIF_PATH_KEY: SAXIF_PATH}


def filter_with_key(key):
    return SAXIF_PATH_KEY + ":" + key
