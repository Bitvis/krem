

import sys
import os
from krempack.core import kjob as krem
from library.returncodes import *

if __name__ == '__main__':
    path, job_name = os.path.split(os.path.dirname(__file__))
    job = krem.Job(job_name, rc)

    job.start()
    
    err = job.run_task_serial('simple_task', 'run')

    for i in range (0,10):
        job.run_task_parallel('simple_task', 'run')
        job.update_on_complete()
    job.end()
    
    ret = job.get_job_result()
    
    exit(ret)
    
