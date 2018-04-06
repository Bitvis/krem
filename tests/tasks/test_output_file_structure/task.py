#!/bin/env python
import os
import re

from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task):

    path = os.path.abspath(os.path.join(p.TEMP_PROJECT_PATH, p.OUTPUT_DIR_NAME))
    result = rc.PASS
    start_directory = os.getcwd()

    dir_content = []
    missing_dir_content = []
    extra_dir_content = []
    job_instance = None
    
    # Navigate to temp project dir and run
    try:
        os.chdir(path)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + path + "'")
        
    if result == rc.PASS:
        print("Changed directory to " + str(path))
        print("Checking contents of directory: " + str(path))
        
        # Get job instance name
        job_instance_temp = f.find_output_job_instance(os.path.join(path, p.SIMPLE_JOB))
        result = job_instance_temp[0]    
            
        if result != rc.FAIL:
            job_instance = job_instance_temp[1]
            # Check dirs
            for dir in p.EXPECTED_OUTPUT_DIRS:
                dir = dir.replace("job_instance", job_instance)
                if not os.path.isdir(dir):
                    result = rc.FAIL
                    print("ERROR: Directory not found: " + str(dir))
        if result != rc.FAIL:
            print("Dir structure OK!")

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))
    
    return(result)

