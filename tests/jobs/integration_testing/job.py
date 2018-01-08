#!/usr/bin/env python

import sys
import os
import time
from krempack.core import kjob as krem
from library.returncodes import *

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".."))
from library.testlib import parameters as p

if __name__ == '__main__':
    path, job_name = os.path.split(os.path.dirname(__file__))
    job = krem.Job(job_name, rc)

    # Initialize job
    job.start()
    
    job.config.job_logger.set_log_level('debug')


    job.run_task_serial('test_command_list_jobs', 'run')
    job.run_task_serial('test_command_list_tasks', 'run')
    
    job.run_task_serial('test_feature_pass_variables', 'run_named_variables', variables=[("test_var_1", p.test_var_1,), ("test_var_2", p.test_var_2)])
    var_list_rc = job.run_task_serial('test_feature_pass_variables', 'run_variable_list', variables=[p.test_var_1, p.test_var_2])
    
    if not var_list_rc:
        temp_project_path = ("path", p.TEMP_PROJECT_PATH)
        if not job.run_task_serial('create_temp_krem_project', 'run', variables=[temp_project_path]):
            if not job.run_task_serial('test_initiated_project', 'run', variables=[temp_project_path]):
                job.run_task_serial('test_output_file_structure', 'run', variables=[temp_project_path])
                job.run_task_serial('test_output_run_log', 'run', variables=[temp_project_path])
                job.run_task_serial('test_output_task_log', 'run', variables=[temp_project_path])
                job.run_task_serial('test_output_results_log', 'run', variables=[temp_project_path])
                if not job.run_task_serial('test_feature_runtime_plugins', 'mv_files_to_krem_temp_project', variables=[temp_project_path]):
                    time.sleep(1) # Fail to create output dir for task if same timestamp
                    job.run_task_serial('test_feature_runtime_plugins', 'test_all_entrypoints', variables=[temp_project_path])
                    time.sleep(1)
                    job.run_task_serial('test_feature_runtime_plugins', 'test_call_order', variables=[temp_project_path])

            job.run_task_serial('remove_temp_krem_project', 'run', variables=[temp_project_path])

    job.run_task_serial('test_command_init_job', 'run')
    job.run_task_serial('test_command_init_task', 'run')
    job.run_task_serial('test_setup_task', 'run')
    
    # Finalize job
    job.end()
    
    ret = job.get_job_result()
    
    exit(ret)
    
