#!/bin/env python
import os

from distutils.dir_util import copy_tree
from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f

this_file_path = os.path.dirname(os.path.realpath(__file__))

test_task_path = os.path.join(this_file_path, "test_files", "test_syntax_error_task")
test_job_path = os.path.join(this_file_path, "test_files", "test_syntax_error_job")



def mv_files_to_krem_temp_project(path):
    test_task_output_path = os.path.realpath(os.path.join(path, p.TASKS_DIR_NAME, "test_syntax_error_task"))
    test_job_output_path = os.path.realpath(os.path.join(path, p.JOBS_DIR_NAME, "test_syntax_error_job"))

    result = rc.PASS
    start_directory = os.getcwd()

    # Navigate to temp project dir and run
    try:
        os.chdir(path)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + path + "'")

    if not result:
        print("Changed directory to " + str(path))

        try:
            copy_tree(test_task_path, test_task_output_path)
            copy_tree(test_job_path, test_job_output_path)
            print("Copied: ")
            print(test_task_path + " -> " + test_task_output_path)
            print(test_job_path + " -> " + test_job_output_path)
        except Exception as e:
            print("ERROR: Failed to copy files")
            print(str(e))
            result = rc.FAIL

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))

    return (result)


def run_with_syntax_error(task, path):
    path = os.path.abspath(path)
    result = rc.PASS
    start_directory = os.getcwd()

    # Navigate to temp project dir and run
    try:
        os.chdir(path)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + path + "'")

    result = mv_files_to_krem_temp_project(path)

    if not result:
        print("Changed directory to " + str(path))
        shell_return = f.shell_run("krem " + p.CMD_RUN + " " + p.CMD_RUN_OPTION_JOB + " " + "test_syntax_error_job")

        #we expect the above command to fail since we are running a job with a task with syntax error
        #so failed job means that this test pass
        if shell_return[0] == 1:
            result = rc.PASS
        else:
            result = rc.FAIL

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))

    return (result)