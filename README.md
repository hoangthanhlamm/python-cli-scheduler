# Python Scheduler

A Python library supporting task scheduling.

## Installation

Install the package using `pip`:

```shell
pip install python-cli-scheduler
```

## Schedule Format

The scheduler format defines how tasks are executed. Use:

```
^<run_now>@<interval>/<delay>$<end_timestamp>#<retry>
```

### Parameters

| Parameter       | Description                                                         | Default |
|-----------------|---------------------------------------------------------------------|---------|
| `run_now`       | Whether to execute immediately (`True` or `False`).                 | `True`  |
| `interval`      | Number of seconds to repeat the task. If `None`, it runs only once. | `None`  |
| `delay`         | Seconds to wait in each interval before executing.                  | `0`     |
| `end_timestamp` | UNIX timestamp to stop execution. If `None`, runs infinitely.       | `None`  |
| `retry`         | Retry execution if an exception occurs (`True` or `False`).         | `True`  |

## Usage

### Use a Decorator

You can use the `scheduler_handle` decorator to execute recurring tasks. Below is an example that prints a random "lucky number" every **10 seconds**, starting at the 3rd second, and continues for 30 seconds.

```python
import random
import time

from cli_scheduler import scheduler_handle

end_time = int(time.time()) + 30


@scheduler_handle(schedule=f'^true@10/3${end_time}#true')
def rotation_lucky(start=0, end=1000):
    n = random.randint(start, end)
    print(f'The lucky number is {n}')


if __name__ == '__main__':
    rotation_lucky(10, end=100)
```

### Using a Scheduler Job Class

With `SchedulerJob`, you gain more control over the task execution lifecycle. This example runs a job every **60 seconds**, starting at the 3rd second, for 5 minutes. It logs the task lifecycle phases and prints a "lucky number."

```python
import time
import random

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
```

## Features
- **Task Scheduling**: Automates task execution using a flexible crontab-like syntax.
- **Decorator Support**: Simplifies task scheduling using Python function decorators.
- **Lifecycle Hooks**: Gain fine-grained control with `SchedulerJob` methods:
    - `_pre_start`: Preparation before starting the task.
    - `_start`: Runs once before task execution begins.
    - `_execute`: The core task logic is implemented here.
    - `_end`: Final cleanup after task execution ends.
    - `_follow_end`: Actions to follow the end of the task lifecycle.

- **Retry Support**: Retry tasks in case of runtime exceptions.

## License
This library is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing
Contributions are welcome! Feel free to submit issues, feature requests, or pull requests to improve the library.
