

from krempack.core import kjob
from library.returncodes import *

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)

    job.start()
    
    err = job.run_task_serial('simple_task', 'run')

    for i in range (0,10):
        job.run_task_parallel('simple_task', 'run')

    job.wait_for_complete()

    job.end()

    task_results = job.get_task_results()

    #we expect each result to be '0' so if the sum of all results is more than 0 then at least one of the tasks failed
    if sum(task_results) > 0:
            err = rc.FAIL

    exit(err)
