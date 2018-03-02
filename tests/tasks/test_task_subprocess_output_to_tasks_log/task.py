#!/bin/env python
from library.returncodes import *
import subprocess
import os
import re

def run_subprocess(task):
    cmd = "ls"

    out = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw_output = out.communicate()
    output = []
    output.append(raw_output[0].decode('utf-8'))
    output.append(raw_output[1].decode('utf-8'))

    print(str(output[0]))
    print(str(output[1]))


    if out.returncode != 0:
        err = rc.FAIL
    else:
        #we expect the following text to be added to the tasks.log file:
        '''    
                19_1    config
                19_1    __init__.py
                19_1    jobs
                19_1    library
                19_1    output
                19_1    tasks
        '''

        #get path to the tasks.log file
        output_path = task.get_output_path()
        tasks_log = os.path.join(output_path, "..", "tasks.log")

        #get task full run number
        run_nr = task.get_full_run_nr()

        tasks_log_file = open(tasks_log, 'r')
        log = tasks_log_file.read()
        tasks_log_file.close()

        # we make it easy and test only for the first line "19_1    config"
        regex = r"" + run_nr + r"  config"

        matches = []
        matches = re.findall(regex, log)

        if len(matches):
            err = rc.PASS
        else:
            err = rc.FAIL

        print(matches)


    return(err)
