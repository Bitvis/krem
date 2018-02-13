#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task, path):
    path = os.path.abspath(path)
    result = rc.PASS
    # Init test project    
    shell_return = f.shell_run("krem " + p.CMD_INIT + " " + p.CMD_INIT_OPTION_PROJECT + " " + path)
    if shell_return[0] != 0:
        result = rc.FAIL
    
    # Copy job and task to test project
    if not result:
        shell_return = f.shell_run("cp -r " + os.path.join(p.TEST_PROJECT_TASKS_DIR, p.SIMPLE_TASK) + " " + os.path.join(path, p.TASKS_DIR_NAME))
        if shell_return[0] != 0:
            result = rc.FAIL

    if not result:
        shell_return = f.shell_run("cp -r " + os.path.join(p.TEST_PROJECT_JOBS_DIR, p.SIMPLE_JOB) + " " + os.path.join(path, p.JOBS_DIR_NAME))
        if shell_return[0] != 0:
            result = rc.FAIL
            
    return result