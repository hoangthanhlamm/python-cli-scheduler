import time

from examples.rotation_luck_job import RotationLuckJob


def test_scheduler_job_repeat():
    end_time = int(time.time()) + 30

    job = RotationLuckJob(scheduler=f'^false@10/3${end_time}#false')
    job.run()


def test_scheduler_job_():
    job = RotationLuckJob(scheduler='^true#true')
    job.run()
