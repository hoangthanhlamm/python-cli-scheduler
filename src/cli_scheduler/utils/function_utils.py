import time

from cli_scheduler.utils.time_utils import round_timestamp


def call_function(f, *args, **kwargs):
    interval = kwargs.get('interval')
    from_start = kwargs.get('from_start', False)
    if from_start:
        next_synced_timestamp = round_timestamp(int(time.time()), round_time=interval) + interval
        f(*args, **kwargs)
    else:
        f(*args, **kwargs)
        next_synced_timestamp = round_timestamp(int(time.time()), round_time=interval) + interval
    return next_synced_timestamp
