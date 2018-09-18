from datetime import datetime

time_zone = -7
commit_time_stamps_formatter = "%Y-%m-%d %H:%M:%S"


def compare_commit_time(left, right):
    # -7 is for remove time zone
    left_strip = datetime.strptime(left[:time_zone], commit_time_stamps_formatter)
    right_strip = datetime.strptime(right[:time_zone], commit_time_stamps_formatter)
    if left_strip > right_strip:
        return left
    elif right_strip > left_strip:
        return right
    else:
        return None

