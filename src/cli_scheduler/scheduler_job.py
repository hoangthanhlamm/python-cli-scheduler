import re
import time
from typing import Union

from cli_scheduler.constants.time_constants import SLEEP_DURATION, TimeInterval
from cli_scheduler.utils.logger_utils import get_logger
from cli_scheduler.utils.time_utils import round_timestamp, human_readable_time

scheduler_format = '^<run_now>@<interval>/<delay>$<end_timestamp>#<retry>'


def scheduler_kwargs(scheduler_str: str):
    def to_bool(d_str: str) -> bool:
        if d_str.lower() == 'false' or d_str == '0':
            return False
        return True

    def to_int(d_str: str, default=None) -> Union[None, int]:
        if d_str.isnumeric():
            return int(d_str)
        elif d_str in TimeInterval.mapping:
            return TimeInterval.mapping[d_str]
        elif d_str == '' or d_str.lower() == 'none' or d_str.lower() == 'null':
            return default
        else:
            raise ValueError(f'Not support interval with {d_str}')

    run_now_str = re.search(r'\^([a-zA-Z0-9]*)', scheduler_str)
    run_now = to_bool(run_now_str.group(1)) if run_now_str is not None else True

    interval_str = re.search(r'@([a-zA-Z0-9]*)', scheduler_str)
    interval = to_int(interval_str.group(1), default=None) if interval_str is not None else None

    delay_str = re.search(r'/(\d*)', scheduler_str)
    delay = to_int(delay_str.group(1), default=0) if delay_str is not None else 0

    end_timestamp_str = re.search(r'\$(\d*)', scheduler_str)
    end_timestamp = to_int(end_timestamp_str.group(1), default=None) if end_timestamp_str is not None else None

    retry_str = re.search(r'#([a-zA-Z0-9]*)', scheduler_str)
    retry = to_bool(retry_str.group(1)) if retry_str is not None else True

    return {'run_now': run_now, 'interval': interval, 'delay': delay, 'end_timestamp': end_timestamp, 'retry': retry}


class SchedulerJob:
    """Base for jobs that need to be run continually"""
    def __init__(self, scheduler=None, **kwargs):
        f"""
        Args:
            * scheduler: Scheduler string with format {scheduler_format}
            * interval: Specify the time interval between each job
            * end_timestamp: the timestamp that the job should stop. Left to 'None' if you don't want it to stop
            * retry=True: Determine whether the function should retry if there is an error
            * delay=0: Number of seconds wait before run new execute
            * run_now=True: Run the first execute now
        """
        if scheduler is not None:
            kwargs.update(scheduler_kwargs(scheduler))

        self.interval = kwargs.get('interval')
        self.end_timestamp = kwargs.get('end_timestamp')
        self.retry = kwargs.get('retry', True)
        self.delay = kwargs.get('delay', 0)
        self.run_now = kwargs.get('run_now', True)

        if (not self.run_now) and (self.interval is None):
            raise ValueError('At least one of the two parameters <run_now> and <interval> must be set positive value')

        self.next_synced_timestamp = None

        self.logger = get_logger(self.__class__.__name__)

    def run(self, *args, **kwargs):
        self._pre_start()
        while True:
            # Check run now. If not, wait to the first execute
            if not self.run_now:
                self._get_next_synced_timestamp()
                if self._check_finish():
                    break
                self._wait_to_next_synced()

            try:
                self._start()
                self._execute(*args, **kwargs)
            except Exception as ex:
                self._handle_exception(ex)
                if self.retry:
                    self._retry()
                    self.run_now = True  # To retry now
                    continue

            self.run_now = False  # To wait for the next execute
            self._end()

        self._follow_end()

    def _get_next_synced_timestamp(self):
        if self.interval is not None:
            self.next_synced_timestamp = round_timestamp(
                self.next_synced_timestamp or int(time.time()), round_time=self.interval) + self.interval + self.delay

        # Get the next execute timestamp
        return self.next_synced_timestamp

    def _wait_to_next_synced(self):
        # Sleep to next execute time
        time_sleep = self.next_synced_timestamp - time.time()
        if time_sleep > 0:
            self.logger.info(f'Waiting {round(time_sleep, 3)} seconds to the next execute [{human_readable_time(self.next_synced_timestamp)}]')
            time.sleep(time_sleep)

    def _handle_exception(self, ex):
        self.logger.exception(ex)
        self.logger.warning('Something went wrong!!!')

    def _check_finish(self):
        # Check if not repeat
        if self.interval is None:
            return True

        # Check if over end timestamp
        if (self.end_timestamp is not None) and (self.next_synced_timestamp > self.end_timestamp):
            return True

        return False

    def _retry(self):
        # Do before retry
        self.logger.warning(f'Try again after {SLEEP_DURATION} seconds ...')
        time.sleep(SLEEP_DURATION)

    def _pre_start(self):
        # Declare object variables and prepare data
        pass

    def _start(self):
        # Before execute
        pass

    def _end(self):
        # After execute
        pass

    def _follow_end(self):
        # End job, export results or close connections
        pass

    def _execute(self, *args, **kwargs):
        # Main execute handler
        pass
