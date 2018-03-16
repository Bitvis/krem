


from krempack.core import kjob
from library.returncodes import *
from config.setup_files import setup

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)

    setup.setup_plugins(job.plugin_handler)

    # Initialize job
    job.start()
    
    # Example of how to set configuration (default log level: 'info')
    job.config.job_logger.set_log_level('debug')


    # <return_code> = job.run_task_serial(<task>, <function>, [arguments])
    for i in range(50):
        job.run_task_parallel('test_task', 'test_func')

    err = job.wait_for_complete()
    
    # Finalize job
    job.end()
    

