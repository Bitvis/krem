


from krempack.core import kjob
from library.returncodes import *


if __name__ == '__main__':
    job = kjob.Job(__file__, rc)

    # Initialize job
    job.start()
    
    # Example of how to set configuration (default log level: 'info')
    job.config.job_logger.set_log_level('debug')


    # <return_code> = job.run_task_serial(<task>, <function>, [arguments])
    err = job.run_task_serial('test_syntax_error_task', 'run_with_syntax_error')
    
    # Finalize job
    job.end()
    

    exit(err)
