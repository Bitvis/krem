#!/bin/env python
import os

from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task):
    
    result = rc.PASS
    start_directory = os.getcwd()

    # Navigate to temp project dir and run
    try:
        os.chdir(p.TEMP_PROJECT_PATH)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + p.TEMP_PROJECT_PATH + "'")
        
    if result == rc.PASS:
        print("Changed directory to " + str(p.TEMP_PROJECT_PATH))
        shell_return = f.shell_run(p.KREM_CMD +  p.CMD_RUN + " " + p.CMD_RUN_OPTION_JOB + " " + p.SIMPLE_JOB)
        if shell_return[0] != 0:
            result = rc.FAIL   

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))
    
    return(result)

