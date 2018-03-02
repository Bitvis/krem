#!/bin/env python
import sys
import os
import subprocess
import re

from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task):

    result = rc.PASS

    jobs_in_dir = []
    listed_jobs = []
    missing_from_list = []
    missing_from_jobs_dir = []

    shell_return = f.shell_run(p.KREM_CMD + "list " + p.CMD_LIST_OPTION_JOB)
    if shell_return[0] != 0:
        result = rc.FAIL
    
    if not result:
        # Get list of jobs
        print("Jobs listed:")
        
        jobprint = re.findall(p.LIST_ID_REGEX + '.*', shell_return[1])
        for job in jobprint:
            m = re.search(p.LIST_ID_REGEX, job)
            if m:
                job = job.replace(m.group(), '')
                job = job.strip()
                listed_jobs.append(job)
                print(job)

        # Get jobs in job directory
        jobs_dir = os.listdir(p.TEST_PROJECT_JOBS_DIR) 
        print("\nJobs present in jobs directory:")        
        for job in jobs_dir:
            if os.path.isdir(os.path.join(p.TEST_PROJECT_JOBS_DIR, job)):
                print(job)
                jobs_in_dir.append(job)

    # compile results
    if not result:
        missing_from_list = f.compare_lists(listed_jobs, jobs_in_dir)
        missing_from_jobs_dir = f.compare_lists(jobs_in_dir, listed_jobs)
        
        if len(missing_from_list) > 0:
            print("\nERROR: Files present in jobs dir that was not listed: " + str(missing_from_list))
            result = rc.FAIL
        if len(missing_from_jobs_dir):
            print("\nERROR: Files listed that are not present in jobs dir: " + str(missing_from_jobs_dir))
            result = rc.FAIL


    return(result)

