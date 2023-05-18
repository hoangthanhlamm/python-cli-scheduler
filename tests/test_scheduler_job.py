import time

from examples.rotation_luck_job import RotationLuckJob


def test_scheduler_job_repeat():
    end_time = int(time.time()) + 3 * 60

    job = RotationLuckJob(scheduler=f'^false@60/3${end_time}#false')
    job.run()


def test_scheduler_job_():
    job = RotationLuckJob(scheduler=f'^true#true')
    job.run()
