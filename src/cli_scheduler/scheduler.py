import time
from typing import Optional

from cli_scheduler.utils.logger_utils import get_logger
from cli_scheduler.utils.parse_scheduler_utils import parse_scheduler_kwargs
from cli_scheduler.utils.time_utils import round_timestamp, human_readable_time


class Scheduler:
    def __init__(self, run_now: bool = True, interval: Optional[int] = None, delay: int = 0, end_timestamp: Optional[int] = None, retry: bool = True):
        self.run_now = run_now
        self.interval = interval
        self.delay = delay
        self.end_timestamp = end_timestamp
        self.retry = retry

        self.next_run_timestamp = None

        self.logger = get_logger(self.__class__.__name__)

    def __str__(self):
        return f'Scheduler(run_now={self.run_now}, interval={self.interval}, delay={self.delay}, end_timestamp={self.end_timestamp}, retry={self.retry})'

    def get_next_run_timestamp(self):
        if self.interval is None:
            return None

        self.next_run_timestamp = round_timestamp(
            self.next_run_timestamp or int(time.time()), round_time=self.interval) + self.interval + self.delay

        # Get the next execute timestamp
        return self.next_run_timestamp

    def wait_to_next_run(self):
        # Sleep to next execute time
        time_sleep = self.next_run_timestamp - time.time()
        if time_sleep > 0:
            self.logger.info(f'Waiting {round(time_sleep, 3)} seconds to the next execute [{human_readable_time(self.next_run_timestamp)}]')
            time.sleep(time_sleep)

    def check_stop(self):
        # Check if not repeat
        if self.interval is None:
            return True

        # Check if over end timestamp
        if (self.end_timestamp is not None) and (self.next_run_timestamp > self.end_timestamp):
            return True

        return False

    def disable_logger(self):
        self.logger.disabled = True

def generate_scheduler(schedule: str) -> Scheduler:
    scheduler_kwargs = parse_scheduler_kwargs(schedule)
    return Scheduler(**scheduler_kwargs)
