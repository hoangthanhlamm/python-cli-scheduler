from cli_scheduler.constants.time_constants import TimeConstants


def round_timestamp(timestamp, round_time=TimeConstants.A_DAY):
    timestamp = int(timestamp)
    timestamp_unit_day = timestamp / round_time
    recover_to_unit_second = int(timestamp_unit_day) * round_time
    return recover_to_unit_second
