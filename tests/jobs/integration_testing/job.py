

import sys
import os
import time
from krempack.core import kjob
from library.returncodes import *

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".."))
from library.testlib import parameters as p

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)

    # Initialize job
    job.start()
    
    job.config.job_logger.set_log_level('info')


    job.run_task_serial('test_command_list_jobs', 'run')
    job.run_task_serial('test_command_list_tasks', 'run')
    
    job.run_task_serial('test_feature_pass_arguments', 'run_named_arguments', arguments=[("test_arg_1", p.test_arg_1,), ("test_arg_2", p.test_arg_2)])

    job.run_task_serial('test_feature_pass_arguments', 'run_with_argument_dict', arguments=p.test_arg_dict)
    job.run_task_serial('test_feature_pass_arguments', 'run_argument_single', arguments=p.test_arg_1)

    arg_list_rc = job.run_task_serial('test_feature_pass_arguments', 'run_argument_list', arguments=[p.test_arg_1, p.test_arg_2])


    if not arg_list_rc:
        temp_project_path = ("path", p.TEMP_PROJECT_PATH)

        job.run_task_serial('remove_temp_krem_project', 'run', arguments=[temp_project_path])

        if not job.run_task_serial('create_temp_krem_project', 'run', arguments=[temp_project_path]):
            if not job.run_task_serial('test_initiated_project', 'run', arguments=[temp_project_path]):
                job.run_task_serial('test_output_file_structure', 'run', arguments=[temp_project_path])
                job.run_task_serial('test_output_run_log', 'run', arguments=[temp_project_path])
                job.run_task_serial('test_output_task_log', 'run', arguments=[temp_project_path])
                job.run_task_serial('test_output_results_log', 'run', arguments=[temp_project_path])

                job.run_task_serial('test_syntax_error_in_task', 'run_with_syntax_error', arguments=[temp_project_path])

                if not job.run_task_serial('test_feature_runtime_plugins', 'mv_files_to_krem_temp_project', arguments=[temp_project_path]):
                    time.sleep(1) # Fail to create output dir for task if same timestamp
                    job.run_task_serial('test_feature_runtime_plugins', 'test_all_hooks', arguments=[temp_project_path])
                    time.sleep(1)
                    job.run_task_serial('test_feature_runtime_plugins', 'test_call_order', arguments=[temp_project_path])

    job.run_task_serial('test_command_init_job', 'run')
    job.run_task_serial('test_command_init_task', 'run')
    job.run_task_serial('test_task_object_in_task', 'run')
    job.run_task_serial('test_task_subprocess_output_to_tasks_log', 'run_subprocess')

    
    # Finalize job
    job.end()

    task_results = job.get_task_results()
    #we expect each result to be '0' so if the sum of all results is more than 0 then at least one of the tasks failed
    if sum(task_results) > 0:
        err = rc.FAIL
    else:
        err = rc.PASS
    
    exit(err)
    
