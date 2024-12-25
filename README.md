# CLI Scheduler

Library support scheduling of task via command line interface.

## Installation
```shell
pip3 install python-cli-scheduler
```

## Usage

Scheduler format: `^<run_now>@<interval>/<delay>$<end_timestamp>#<retry>`

Parameters:

- `run_now`: Execute now. Default: `True`
- `interval`: Repeat execute after number of seconds. If set to `None`, execute one time and not repeat. Default: `None`
- `delay`: Execute at second `delay`-th at each interval. Default: `0
- `end_time`: Execute until `end_time`. If set to `None`, infinite repeat. Default: `None`
- `retry`: Retry if exception when executed. Default: `True`

### Use with decorator

Coming soon

### Use with scheduler job class

Example job to print a lucky number at second 3 every minute.

```python
import time
import random

from cli_scheduler.scheduler_job import SchedulerJob


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
```