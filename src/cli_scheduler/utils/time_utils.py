from datetime import datetime

from cli_scheduler.constants.time_constants import TimeConstants


def round_timestamp(timestamp, round_time=TimeConstants.A_DAY):
    timestamp = int(timestamp)
    timestamp_unit_day = timestamp / round_time
    recover_to_unit_second = int(timestamp_unit_day) * round_time
    return recover_to_unit_second


def human_readable_time(timestamp):
    t = datetime.fromtimestamp(timestamp)
    return t.strftime('%d-%m-%Y %H:%M:%S')
