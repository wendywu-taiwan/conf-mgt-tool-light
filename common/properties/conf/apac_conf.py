from common.properties.region_setting import REGION_APAC, TIME_ZONE_SET

CURRENT_REGION = REGION_APAC
CURRENT_TIME_ZONE = TIME_ZONE_SET.get(CURRENT_REGION)
STATIC_URL = "/apac/static/"
URL_PRE_PATH = "apac/"
PRELOAD_DATA = "preload_data_apac.json"
AUTH_DATA = "auth_data_apac.json"
