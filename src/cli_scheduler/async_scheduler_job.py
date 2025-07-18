import asyncio
import time

from cli_scheduler.constants.time_constants import SLEEP_DURATION
from cli_scheduler.utils.logger_utils import get_logger
from cli_scheduler.utils.parse_scheduler_utils import parse_scheduler_kwargs, scheduler_format
from cli_scheduler.utils.time_utils import round_timestamp, human_readable_time


class AsyncSchedulerJob:
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
            kwargs.update(parse_scheduler_kwargs(scheduler))

        self.interval = kwargs.get('interval')
        self.end_timestamp = kwargs.get('end_timestamp')
        self.retry = kwargs.get('retry', True)
        self.delay = kwargs.get('delay', 0)
        self.run_now = kwargs.get('run_now', True)

        if (not self.run_now) and (self.interval is None):
            raise ValueError('At least one of the two parameters <run_now> and <interval> must be set positive value')

        self.next_synced_timestamp = None

        self.logger = get_logger(self.__class__.__name__)

    async def run(self, *args, **kwargs):
        await self._pre_start()
        while True:
            # Check run now. If not, wait for the first execution
            if not self.run_now:
                self._get_next_synced_timestamp()
                if self._check_finish():
                    break
                await self._wait_to_next_synced()

            try:
                await self._start()
                await self._execute(*args, **kwargs)
            except Exception as ex:
                await self._handle_exception(ex)
                if self.retry:
                    await self._retry()
                    self.run_now = True  # To retry now
                    continue

            self.run_now = False  # To wait for the next execution
            await self._end()

        await self._follow_end()

    def _get_next_synced_timestamp(self):
        if self.interval is not None:
            self.next_synced_timestamp = round_timestamp(
                self.next_synced_timestamp or int(time.time()), round_time=self.interval) + self.interval + self.delay

        # Get the next execution timestamp
        return self.next_synced_timestamp

    def _check_finish(self):
        # Check if not repeat
        if self.interval is None:
            return True

        # Check if over end timestamp
        if (self.end_timestamp is not None) and (self.next_synced_timestamp > self.end_timestamp):
            return True

        return False

    async def _wait_to_next_synced(self):
        # Sleep to next execute time
        time_sleep = self.next_synced_timestamp - time.time()
        if time_sleep > 0:
            self.logger.info(f'Waiting {round(time_sleep, 3)} seconds to the next execute [{human_readable_time(self.next_synced_timestamp)}]')
            await asyncio.sleep(time_sleep)

    async def _handle_exception(self, ex):
        self.logger.exception(ex)
        self.logger.warning('Something went wrong!!!')

    async def _retry(self):
        # Do before retry
        self.logger.warning(f'Try again after {SLEEP_DURATION} seconds ...')
        await asyncio.sleep(SLEEP_DURATION)

    async def _pre_start(self):
        # Declare object variables and prepare data
        pass

    async def _start(self):
        # Before execution
        pass

    async def _end(self):
        # After execution
        pass

    async def _follow_end(self):
        # End job, export results or close connections
        pass

    async def _execute(self, *args, **kwargs):
        # Main execute handler
        pass
