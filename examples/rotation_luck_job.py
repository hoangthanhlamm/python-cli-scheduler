import random
import time

from cli_scheduler import SchedulerJob


class RotationLuckJob(SchedulerJob):
    def __init__(self, scheduler):
        super().__init__(scheduler=scheduler)

    def _pre_start(self):
        self.logger.info('Rotation luck. Have fun !')

    def _start(self):
        self.n = random.randint(0, 1000)

    def _execute(self, *args, **kwargs):
        self.logger.info(f'The lucky number is {self.n}')

    def _end(self):
        del self.n

    def _follow_end(self):
        self.logger.info('Done')


if __name__ == '__main__':
    end_time = int(time.time()) + 5 * 60

    # ^false: Not execute now
    # @60: Repeat execute every 60 second
    # /3: Execute at second 3
    # ${end_time}: Run until end_time
    # #false: Don't retry if exception when execute
    job = RotationLuckJob(scheduler=f'^false@60/3${end_time}#false')
    job.run()
