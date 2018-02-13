#!/bin/env python
import shutil
import os
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task):
    result = rc.PASS
    temp_task_created = False
    temp_task_path = os.path.join(p.TEST_PROJECT_TASKS_DIR, p.TEMP_TASK_NAME)
    
    # Init job    
    shell_return = f.shell_run("krem " + p.CMD_INIT + " " + p.CMD_INIT_OPTION_TASK + " " + p.TEMP_TASK_NAME)
    if shell_return[0] != 0:
        result = rc.FAIL
    else: 
        temp_task_created = True
        
    if not result:
        if not os.path.isfile(os.path.join(temp_task_path, p.TASK_SCRIPT)):
            result = rc.FAIL
            print("ERROR: Failed to deploy task template file: " + p.TASK_SCRIPT)

    if temp_task_created:
        try:
            shutil.rmtree(temp_task_path)
            print("Directory removed: " + str(temp_task_path))
        except Exception:
            print("WARNING: Failed to remove temporary task '" + p.TEMP_TASK_NAME + "'")
            result = rc.UNSTABLE
            
    return result

