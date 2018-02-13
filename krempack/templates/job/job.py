


from krempack.core import kjob
from library.returncodes import *
from library.setup import setup_plugins

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)

    # Setup plugins
    setup_plugins(job.plugin_handler)

    # Initialize job
    job.start()
    
    # Example of how to set logging level (default level: 'info', debug level: 'debug')
    job.config.job_logger.set_log_level('info')


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
    tasks_results is a list of all return codes from the parallel tasks
    '''
    task_results = job.wait_for_complete() # Wait until parallel tasks are complete, and return results


    '''
    get results from all tasks as a list
    '''
    all_task_results = job.get_task_results()

    
    # Finalize job
    job.end()


    #return an appropriate return code
    exit(rc.PASS)
    
