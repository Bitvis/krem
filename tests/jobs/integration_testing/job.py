

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
    job.run_task_serial('test_feature_pass_arguments', 'run_with_argument_int', arguments=p.test_arg_int)
    job.run_task_serial('test_feature_pass_arguments', 'run_with_argument_float', arguments=p.test_arg_float)


    ret, var = job.run_task_serial('test_vars_from_job_to_task', 'return_single_variable')
    job.run_task_serial('test_vars_from_job_to_task', 'check_vars', arguments=[('test', 'return_single_variable'), ('var_ret', ret), ('var', var)])

    ret, var = job.run_task_serial('test_vars_from_job_to_task', 'return_list_variable')
    job.run_task_serial('test_vars_from_job_to_task', 'check_vars', arguments=[('test', 'return_list_variable'), ('var_ret', ret), ('var', var)])

    ret, var = job.run_task_serial('test_vars_from_job_to_task', 'return_three_variables')
    job.run_task_serial('test_vars_from_job_to_task', 'check_vars', arguments=[('test', 'return_three_variables'), ('var_ret', ret), ('var', var)])

    # fire off some parallel tasks
    job.run_task_parallel('test_vars_from_job_to_task', 'return_single_variable')
    job.run_task_parallel('test_vars_from_job_to_task', 'return_list_variable')
    job.run_task_parallel('test_vars_from_job_to_task', 'return_object')
    return_codes, return_vars = job.wait_for_complete()

    # now test that the variables from the above parallel tasks are correct
    job.run_task_serial('test_vars_from_job_to_task', 'check_vars', arguments=[('test', 'return_single_variable'), ('var_ret', ret), ('var', return_vars[0])])
    job.run_task_serial('test_vars_from_job_to_task', 'check_vars', arguments=[('test', 'return_list_variable'), ('var_ret', ret), ('var', return_vars[1])])
    job.run_task_serial('test_vars_from_job_to_task', 'check_vars', arguments=[('test', 'return_object'), ('var_ret', ret), ('var', return_vars[2])])


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
                    time.sleep(1)
                    job.run_task_serial('test_feature_runtime_plugins', 'test_pass_data', arguments=[temp_project_path])
                    time.sleep(1)
                    job.run_task_serial('test_feature_runtime_plugins', 'test_pass_data_parallel', arguments=[temp_project_path])

                if not job.run_task_serial('test_feature_cli_plugins', 'mv_files_to_krem_temp_project', arguments=[temp_project_path]):
                    time.sleep(1) # Fail to create output dir for task if same timestamp
                    job.run_task_serial('test_feature_cli_plugins', 'test_command_hook', arguments=[temp_project_path])
                    job.run_task_serial('test_feature_cli_plugins', 'test_argument_setup_hooks', arguments=[temp_project_path])
                    job.run_task_serial('test_feature_cli_plugins', 'test_argument_execute_hooks', arguments=[temp_project_path])

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
    
