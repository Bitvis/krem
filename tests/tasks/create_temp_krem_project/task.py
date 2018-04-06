#!/bin/env python

import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task):
    
    result = rc.PASS
    # Init test project    
    shell_return = f.shell_run(p.KREM_CMD + p.CMD_INIT + " " + p.CMD_INIT_OPTION_PROJECT + " " + p.TEMP_PROJECT_PATH)

    print(p.TEMP_PROJECT_PATH)
    if shell_return[0] != 0:
        result = rc.FAIL
    
    # Copy job and task to test project
    if result == rc.PASS:
        shell_return = f.shell_run("cp -r " + os.path.join(p.TEST_PROJECT_TASKS_DIR, p.SIMPLE_TASK) + " " + os.path.join(p.TEMP_PROJECT_PATH, p.TASKS_DIR_NAME))
        if shell_return[0] != 0:
            result = rc.FAIL

    if result == rc.PASS:
        shell_return = f.shell_run("cp -r " + os.path.join(p.TEST_PROJECT_JOBS_DIR, p.SIMPLE_JOB) + " " + os.path.join(p.TEMP_PROJECT_PATH, p.JOBS_DIR_NAME))
        if shell_return[0] != 0:
            result = rc.FAIL
            
    return result