#!/bin/env python
import shutil
import os
from library.task import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run():
    result = rc.PASS
    temp_job_created = False
    temp_job_path = os.path.join(p.TEST_PROJECT_JOBS_DIR, p.TEMP_JOB_NAME)
    
    # Init job    
    shell_return = f.shell_run("krem " + p.CMD_INIT + " " + p.CMD_INIT_OPTION_JOB + " " + p.TEMP_JOB_NAME)
    if shell_return[0] != 0:
        result = rc.FAIL
    else: 
        temp_job_created = True
        
    if not result:
        if not os.path.isfile(os.path.join(temp_job_path, p.DEAFULT_JOB_SCRIPT)):
            result = rc.FAIL
            print("ERROR: Failed to deploy job template")
        
    if temp_job_created:
        try:
            shutil.rmtree(temp_job_path)
            print("Directory removed: " + str(temp_job_path))
        except Exception:
            print("WARNING: Failed to remove temporary job '" + p.TEMP_JOB_NAME + "'")
            result = rc.UNSTABLE
            
    return result
