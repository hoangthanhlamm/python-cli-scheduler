import time
from functools import wraps

from cli_scheduler.constants.time_constants import SLEEP_DURATION
from cli_scheduler.scheduler import Scheduler, generate_scheduler


def scheduler_handle(schedule=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            scheduler: Scheduler = generate_scheduler(schedule)

            while True:
                # Check run now. If not, wait to the first execute
                if not scheduler.run_now:
                    scheduler.get_next_run_timestamp()
                    if scheduler.check_stop():
                        break
                    scheduler.wait_to_next_run()

                try:
                    f(*args, **kwargs)
                except Exception as ex:
                    scheduler.logger.exception(ex)

                    if scheduler.retry:
                        scheduler.logger.warning(f'Try again after {SLEEP_DURATION} seconds ...')
                        time.sleep(SLEEP_DURATION)
                        scheduler.run_now = True  # To retry now
                        continue

                scheduler.run_now = False  # To wait for the next execute

        return decorated_function

    return decorator
