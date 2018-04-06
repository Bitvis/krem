#!/bin/env python
import os
import shutil
from distutils.dir_util import copy_tree

from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import platform

this_file_path = os.path.dirname(os.path.realpath(__file__))

test_task_path = os.path.join(this_file_path, "..", "..", "library", "testlib", "test_task")
test_job_path = os.path.join(this_file_path, "..", "..", "library", "testlib", "test_job")
test_job_par_path = os.path.join(this_file_path, "..", "..", "library", "testlib", "test_job_par")
test_plugin_setup_files = os.path.join(this_file_path, "test_files", "plugin_files", "setup_files")
test_plugins = os.path.join(this_file_path, "test_files", "plugin_files", "plugins")

def mv_files_to_temp_krem_project(task):
    test_task_output_path = os.path.realpath(os.path.join(p.TEMP_PROJECT_PATH, p.TASKS_DIR_NAME, "test_task"))
    test_job_output_path = os.path.realpath(os.path.join(p.TEMP_PROJECT_PATH, p.JOBS_DIR_NAME, "test_job"))
    test_job_par_output_path = os.path.realpath(os.path.join(p.TEMP_PROJECT_PATH, p.JOBS_DIR_NAME, "test_job_par"))
    test_plugin_setup_output_path = os.path.realpath(os.path.join(p.TEMP_PROJECT_PATH, p.CONFIG_DIR_NAME, "setup_files"))
    test_plugins_output_path = os.path.realpath(os.path.join(p.TEMP_PROJECT_PATH, p.LIBRARY_DIR_NAME, "plugins"))


    result = rc.PASS
    start_directory = os.getcwd()

    # Navigate to temp project dir and run
    try:
        os.chdir(p.TEMP_PROJECT_PATH)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + p.TEMP_PROJECT_PATH + "'")

    if result == rc.PASS:
        print("Changed directory to " + str(p.TEMP_PROJECT_PATH))
        
        try:
            copy_tree(test_task_path, test_task_output_path)
            copy_tree(test_job_path, test_job_output_path)
            copy_tree(test_job_par_path, test_job_par_output_path)
            copy_tree(test_plugin_setup_files, test_plugin_setup_output_path)
            copy_tree(test_plugins, test_plugins_output_path)
            print("Copied: ")
            print(test_task_path + " -> " + test_task_output_path)
            print(test_job_path + " -> " + test_job_output_path)
            print(test_job_par_path + " -> " + test_job_par_output_path)
            print(test_plugin_setup_files + " -> " + test_plugin_setup_output_path)
            print(test_plugins + " -> " + test_plugins_output_path)        
        except Exception as e:
            print("ERROR: Failed to copy files")
            print(str(e))
            result = rc.FAIL

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))

    return(result)

def execute_with_target_setup(path, target, test_job):
    result = rc.PASS
    setup_path = os.path.join(p.CONFIG_DIR_NAME, "setup_files")

    # Navigate to temp project dir and run
    try:
        os.chdir(path)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + path + "'")


    # Rename target setup file to "setup.py"
    if result == rc.PASS:
        print("Changed directory to " + str(path))

        try:
            shutil.move(os.path.join(setup_path, target), os.path.join(setup_path, "setup.py"))
            print("Using setup file: " + target)
        except Exception as e:
            print("Error: Failed to set target setup file: " + target)
            result = rc.FAIL

        #remove setup.pyc
        if os.path.isfile(os.path.join(setup_path, "setup.pyc")):
            os.remove(os.path.join(setup_path, "setup.pyc"))

    # execute job
    if result == rc.PASS:
        shell_return = f.shell_run("krem run -j " + test_job)
        if shell_return[0] != 0:
            result = rc.FAIL

    #rename test file to original name
    try:
        shutil.move(os.path.join(setup_path, "setup.py"), os.path.join(setup_path, target))    
    except Exception as e:
        print("WARNING: Failed to rename setup script back to original name")
        result = rc.UNSTABLE

    return(result)

def test_pass_data(task):
    start_directory = os.getcwd()

    result = execute_with_target_setup(p.TEMP_PROJECT_PATH, "setup_test_data.py", "test_job")
    if result == rc.PASS:
        if not os.path.isfile(os.path.join("output", "task_data_ok")):
            print("Plugin failed to create file: " + "task_data_ok")
            result = rc.FAIL
        if not os.path.isfile(os.path.join("output", "job_data_ok")):
            print("Plugin failed to create file: " + "job_data_ok")
            result = rc.FAIL

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))
    return result

def test_pass_data_parallel(task):
    start_directory = os.getcwd()

    result = execute_with_target_setup(p.TEMP_PROJECT_PATH, "setup_test_data_parallel.py", "test_job_par")
    if result == rc.PASS:
        for i in range(50):
            testline = "task_data_ok_" + str( (i + 1) )
            if not os.path.isfile(os.path.join("output", testline)):
                print("Plugin failed to create file: " + testline)
                result = rc.FAIL

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))
    return result

def test_all_hooks(task):
    start_directory = os.getcwd()

    result = execute_with_target_setup(p.TEMP_PROJECT_PATH, "setup_test_all_hooks.py", "test_job")
    if result == rc.PASS:
        if not os.path.isfile(os.path.join("output", "job_start")):
            print("Plugin failed to create file: " + "job_start")
            result = rc.FAIL
        if not os.path.isfile(os.path.join("output", "pre_task_execution")):
            print("Plugin failed to create file: " + "pre_task_execution")
            result = rc.FAIL
        if not os.path.isfile(os.path.join("output", "job_progress_text")):
            print("Plugin failed to create file: " + "job_progress_text")
            result = rc.FAIL
        if not os.path.isfile(os.path.join("output", "pre_task_function_call")):
            print("Plugin failed to create file: " + "pre_task_function_call")
            result = rc.FAIL
        if not os.path.isfile(os.path.join("output", "post_task_function_call")):
            print("Plugin failed to create file: " + "post_task_function_call")
            result = rc.FAIL
        if not os.path.isfile(os.path.join("output", "post_task_execution")):
            print("Plugin failed to create file: " + "post_task_execution")
            result = rc.FAIL
        if not os.path.isfile(os.path.join("output", "job_end")):
            print("Plugin failed to create file: " + "job_end")
            result = rc.FAIL

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))
    return result

def test_call_order(task):
    start_directory = os.getcwd()
    result = execute_with_target_setup(p.TEMP_PROJECT_PATH, "setup_test_call_order.py", "test_job")
    if result == rc.PASS:
        if not os.path.isfile(os.path.join("output", "call_order_ok")):
            print("ERROR: Failed to verify call order")
            result = rc.FAIL
        else:
            print("Call order verified")
        f.shell_run("cat output/test_job/latest/1_test_task__run__test_func_1/task.log")
    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))
    return result

