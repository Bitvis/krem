#!/usr/bin/env python

import sys
import os
from krempack.core import kjob as krem
from library.returncodes import *
from library.setup import setup_plugins

if __name__ == '__main__':
    path, job_name = os.path.split(os.path.dirname(__file__))
    job = krem.Job(job_name, rc)

    # Setup plugins
    setup_plugins(job.plugin_handler)

    # Initialize job
    job.start()
    
    # Example of how to set configuration (default log level: 'info')
    job.config.job_logger.set_log_level('debug')


    # <return_code> = job.run_task_serial(<task>, <function>, [variables])
    err = job.run_task_serial('example_task', 'example_function_with_variable_list', variables=["variable passed from job", "as list"])

    # Parallel tasks run only if previous task passed
    if not err:    
        #job.run_task_parallel(<task>, <function>, [variables])
        job.run_task_parallel('example_task', 'example_function_with_named_variables', variables=[("var1", ""), ("var2", "run_in_parallel")])
        job.run_task_parallel('example_task', 'example_function_with_named_variables', variables=[("var1", "also"), ("var2", "run_in_parallel")])

        # <return_code> = job.update_on_complete()
        err = job.update_on_complete() # Wait until parallel tasks are complete, and return result

    err = job.run_task_serial('example_task', 'example_function_without_variables')
    
    # Finalize job
    job.end()
    
    #if only a single task returned error code !=0, then return that error code,
    #else if more than one task returned !=0, but the codes are the same for all, then return that code
    #else if more than one task returned !=0, and the codes differ then return 1
    ret = job.get_job_result()
    
    exit(ret)
    
