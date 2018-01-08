#!/usr/bin/env python

import sys
import os
from krempack.core import kjob as krem
from library.returncodes import *
from config.setup_files import setup

if __name__ == '__main__':
    path, job_name = os.path.split(os.path.dirname(__file__))
    job = krem.Job(job_name, rc)

    setup.setup_plugins(job.plugin_handler)

    # Initialize job
    job.start()
    
    # Example of how to set configuration (default log level: 'info')
    job.config.job_logger.set_log_level('debug')


    # <return_code> = job.run_task_serial(<task>, <function>, [variables])
    err = job.run_task_serial('test_plugin_task', 'test_func')
    
    # Finalize job
    job.end()
    
    #if only a single task returned error code !=0, then return that error code,
    #else if more than one task returned !=0, but the codes are the same for all, then return that code
    #else if more than one task returned !=0, and the codes differ then return 1
    ret = job.get_job_result()
    
    exit(ret)
    
