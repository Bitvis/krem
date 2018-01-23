

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


    '''
    adding three tasks to be executed in sequence using job.run_task_serial:
    <return code> = job.run_task_serial(<task>, <function>, [variables])
    '''

    #executing function 'run_without_variables' in task 'example_task'
    err = job.run_task_serial('task_foo', 'run_without_variables')

    if err == rc.PASS:
        #executing a task function with a list of variables
        err = job.run_task_serial('task_foo', 'run_with_variable_list', variables=["variable passed from job", "as list"])

        if err == rc.PASS:
            #executing task function with named variables
            err = job.run_task_serial('task_foo', 'run_with_named_variables', variables=[("var1", "var1_value"), ("var2", "var2_value")])



    '''
    adding two tasks to be executed in parallel using:
    job.run_task_parallel(<task>, <function>, [variables])
    '''
    #job.run_task_parallel(<task>, <function>, [variables])
    job.run_task_parallel('task_foo', 'run_with_named_variables', variables=[("var1", ""), ("var2", "run_in_parallel")])
    job.run_task_parallel('task_foo', 'run_with_named_variables', variables=[("var1", "also"), ("var2", "run_in_parallel")])

    '''
    the below function will trigger execution of parallel tasks and it will return when all parallel tasks finish
    '''
    err = job.update_on_complete() # Wait until parallel tasks are complete, and return result

    
    # Finalize job
    job.end()
    
    #if only a single task returned error code !=0, then return that error code,
    #else if more than one task returned !=0, but the codes are the same for all, then return that code
    #else if more than one task returned !=0, and the codes differ then return 1
    ret = job.get_job_result()
    
    exit(ret)
    
