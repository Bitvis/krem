#!/bin/env python
import os

from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task, path):

    path = os.path.abspath(os.path.join(path, p.OUTPUT_DIR_NAME))
    result = rc.PASS
    start_directory = os.getcwd()
    
    # Navigate to temp project dir and run
    try:
        os.chdir(path)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + path + "'")
        
    if not result:
        print("Changed directory to " + str(path))
        
        job_instance = f.find_output_job_instance(os.path.join(path, p.SIMPLE_JOB))
        result = job_instance[0]    
            
        if result != rc.FAIL:
            file = p.EXPECTED_OUTPUT_FILE_RESULTS.replace("job_instance", job_instance[1])
            result = f.check_file_content(file, p.EXPECTED_CONTENT_RESULTS)
        

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))
    
    return(result)

