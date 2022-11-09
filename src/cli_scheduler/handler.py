from functools import wraps
import time

from cli_scheduler.constants.time_constants import SLEEP_DURATION
from cli_scheduler.utils.function_utils import call_function
from cli_scheduler.utils.logger_utils import get_logger

logger = get_logger('Repeat handler')


def repeat_handler(interval: int = None, end_timestamp: int = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """Schedule function execution after every fixed interval.

            :key interval: (int) Fixed interval.
            :key end_timestamp: (int) Timestamp to finish execute. Default: None.
            :key from_start: (bool) Calculate next run time from start time or not. Default: False.
            """
            kw_interval = interval or kwargs.get('interval')
            kwargs['interval'] = kw_interval

            kw_end_timestamp = end_timestamp or kwargs.get('end_timestamp')
            while True:
                try:
                    next_synced_timestamp = call_function(f, *args, **kwargs)

                    # Check if not repeat
                    if kw_interval is None:
                        return

                    if (kw_end_timestamp is not None) and (next_synced_timestamp > kw_end_timestamp):
                        return

                    # Sleep to next synced time
                    time_sleep = next_synced_timestamp - time.time()
                    if time_sleep > 0:
                        logger.info(f'Sleep {round(time_sleep, 3)} seconds')
                        time.sleep(time_sleep)
                except Exception as ex:
                    logger.exception(ex)
                    logger.warning(f'Something went wrong!!! Try again after {SLEEP_DURATION} seconds ...')
                    time.sleep(SLEEP_DURATION)

        return decorated_function

    return decorator
