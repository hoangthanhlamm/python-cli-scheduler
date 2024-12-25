import random
import time

from cli_scheduler.scheduler_handle import scheduler_handle

end_time = int(time.time()) + 30


@scheduler_handle(schedule=f'^true@10/3${end_time}#true')
def rotation_lucky(start=0, end=1000):
    n = random.randint(start, end)
    print(f'The lucky number is {n}')


if __name__ == '__main__':
    rotation_lucky(10, end=100)
