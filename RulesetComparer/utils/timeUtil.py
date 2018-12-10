import pytz
from datetime import datetime, timezone, timedelta
from RulesetComparer.properties import config


def timestamp_to_time(timestamp, time_format):
    date_time = timestamp_to_date_time(timestamp)
    return date_time_to_time(date_time, time_format)


def time_to_timestamp(time, time_format):
    date_time = time_to_date_time(time, time_format)
    time_stamp = date_time_to_timestamp(date_time)
    return time_stamp


# return timestamp from date time
def date_time_to_timestamp(date_time):
    return date_time.timestamp()


def timestamp_to_date_time(timestamp):
    ts = int(timestamp)
    date_time = datetime.fromtimestamp(ts)

    return date_time


def date_time_change_format(date_time, time_format):
    str_time = date_time.strftime(time_format)
    return time_to_date_time(str_time, time_format)


def date_time_change_time_zone(date_time, time_zone):
    time_zone = pytz.timezone(time_zone)
    return date_time.replace(tzinfo=time_zone)


# return time in specific format
def time_to_date_time(str_time, time_format):
    return datetime.strptime(str_time, time_format)


def date_time_to_time(date_time, time_format):
    time_str = date_time.strftime(time_format)
    return time_str.strip("'")


def date_time_to_date_time(date_time, time_format):
    new_date_time = date_time.strftime(time_format)
    return new_date_time


def timestamp_to_local_time(timestamp):
    time_zone = config.TIME_ZONE.get('asia_taipei')
    return timestamp_to_time(timestamp, time_zone)


# provide date time and hour, return date time add hour
def date_time_add_hour(date_time, hour):
    new_time = date_time
    new_time.replace(hour=hour)
    return hour


def date_time_add_day(date_time):
    tomorrow_time = date_time + timedelta(days=1)
    return tomorrow_time


def date_time_tomorrow_o_clock(date_time, hour):
    tomorrow_time = date_time + timedelta(days=1)
    tomorrow_time.replace(hour=hour)


def get_date_time(time_zone, year=None, month=None, day=None, hour=None, minute=None, second=None):
    current_date_time = get_current_date_time()
    if year is None:
        year = current_date_time.year
    if month is None:
        month = current_date_time.month
    if day is None:
        day = current_date_time.day
    if hour is None:
        hour = current_date_time.hour
    if minute is None:
        minute = current_date_time.minute
    if second is None:
        second = current_date_time.second

    time_zone = pytz.timezone(time_zone)
    new_date_time = datetime(year, month, day, hour, minute, second, tzinfo=time_zone)
    return new_date_time


def get_naive_time(year=None, month=None, day=None, hour=None, minute=None, second=None):
    current_date_time = get_current_date_time()
    if year is None:
        year = current_date_time.year
    if month is None:
        month = current_date_time.month
    if day is None:
        day = current_date_time.day
    if hour is None:
        hour = current_date_time.hour
    if minute is None:
        minute = current_date_time.minute
    if second is None:
        second = current_date_time.second

    new_date_time = datetime(year, month, day, hour, minute, second)
    return new_date_time


# return current time in format ex 1990/12/11 10:32:30
def get_current_time():
    time_format = config.TIME_FORMAT.get('year_month_date_hour_minute_second')
    return get_format_current_time(time_format)


# return current time date time
def get_current_date_time():
    utc_date_time = datetime.utcnow()
    time_zone = config.TIME_ZONE.get('asia_taipei')
    local_time = utc_to_locale_time(utc_date_time, time_zone)
    return local_time


# return current time stamp
def get_current_timestamp():
    utc_date_time = datetime.utcnow()
    return date_time_to_timestamp(utc_date_time)


# get current time with different format
def get_format_current_time(time_format):
    current_date_time = get_current_date_time()
    return date_time_to_time(current_date_time, time_format)


def get_format_time(date_time, time_format):
    time_str = date_time.strftime(time_format)
    return time_str.strip("'")


# transfer utc time to specific timezone
def utc_to_locale_time(utc_date_time, target_time_zone):
    current_time_zone = pytz.timezone('UTC')
    target_time_zone = pytz.timezone(target_time_zone)
    time = current_time_zone.localize(utc_date_time).astimezone(target_time_zone)
    return time


# transfer utc time to specific timezone
def local_time_to_utc(local_time, current_time_zone):
    current_time_zone = pytz.timezone(current_time_zone)
    target_time_zone = pytz.timezone('UTC')
    time = current_time_zone.localize(local_time).astimezone(target_time_zone)
    return time


def compare_git_time(left, right):
    format = config.TIME_FORMAT.get('git_time_format')
    time_zone = -7
    # -7 is for remove time zone
    left_strip = datetime.strptime(left[:time_zone], format)
    right_strip = datetime.strptime(right[:time_zone], format)
    if left_strip > right_strip:
        return left
    elif right_strip > left_strip:
        return right
    else:
        return None


commit_time_stamps_formatter = "%Y-%m-%d %H:%M:%S"
