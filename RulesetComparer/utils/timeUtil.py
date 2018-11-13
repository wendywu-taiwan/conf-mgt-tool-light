import pytz
from datetime import datetime, timezone
from RulesetComparer.properties import config


def get_current_time():
    format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')
    time_zone = config.TIME_ZONE.get('asia_taipei')
    return get_format_locale_time(format, time_zone)


def get_format_locale_time(format, time_zone):
    time = utc_to_locale_time(time_zone)
    time_str = time.strftime(format)
    return time_str.strip("'")


def utc_to_locale_time(time_zone):
    utc_date_time = datetime.utcnow()
    time_zone = pytz.timezone(time_zone)
    time = utc_date_time.replace(tzinfo=timezone.utc).astimezone(tz=time_zone)
    return time
