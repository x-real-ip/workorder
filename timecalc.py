import re
import datetime


def convert_date(date_input):
    """Return date as month with three letters and day as number"""
    date_output = datetime.datetime.strptime(
        date_input, "%Y-%m-%d").strftime("%b " "%-d")
    return date_output


def split_time(time):
    """Return time 'HH', 'MM' as list, any non digit character will be used as seperator"""
    time = re.split("\D", time)
    hours = int(time[0])
    minute = int(time[1])
    return [hours, minute]


def time_round_down(hour, minute):
    """Return time 'HH', 'MM' with minutes rounded down to a quarter"""
    if minute <= 15:
        minute = 00
    elif minute <= 30 >= 15:
        minute = 15
    elif minute <= 45 >= 30:
        minute = 30
    else:
        minute = 45
    return (f"{hour:02d}"), (f"{minute:02d}")


def time_round_up(hour, minute):
    """Return time 'HH', 'MM' with minutes rounded up to a quarter"""
    if minute <= 15 >= 00:
        minute = 15
    elif minute <= 30 >= 15:
        minute = 30
    elif minute <= 45 >= 30:
        minute = 45
    else:
        minute = 00
        hour += 1
        if hour == 24:
            hour = 00
    return (f"{hour:02d}"), (f"{minute:02d}")
