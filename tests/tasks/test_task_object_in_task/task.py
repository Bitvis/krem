#!/bin/env python
import os

from library.returncodes import *





def run(task):
    output_path = task.get_output_path()
    if output_path is None:
        result = rc.FAIL
    else:
        result = rc.PASS
        print(output_path)

    run_name = task.get_run_name()
    if run_name is None:
        result = rc.FAIL
    else:
        result = rc.PASS
        print(run_name)

    task_name = task.get_task_name()
    if task_name is None:
        result = rc.FAIL
    else:
        result = rc.PASS
        print(task_name)

    run_nr = task.get_run_nr()
    if run_nr is None:
        result = rc.FAIL
    else:
        result = rc.PASS
        print(run_nr)

    full_run_nr = task.get_full_run_nr()
    if full_run_nr is None:
        result = rc.FAIL
    else:
        result = rc.PASS
        print(full_run_nr)

    job_path = task.get_job_path()
    if job_path is None:
        result = rc.FAIL
    else:
        result = rc.PASS
        print(job_path)

    return(result)

