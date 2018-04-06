#!/bin/env python
import os

from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f
import shutil
from distutils.dir_util import copy_tree

this_file_path = os.path.abspath(os.path.dirname(__file__))

test_task_path = os.path.join(this_file_path, "..", "..", "library", "testlib", "test_task")
test_job_path = os.path.join(this_file_path, "..", "..", "library", "testlib", "test_job")
test_plugin_setup_file = os.path.join(this_file_path, "test_files", "plugin_files", "setup_files", "setup.py")
test_plugins = os.path.join(this_file_path, "test_files", "plugin_files", "plugins")


def mv_files_to_temp_krem_project(task):
    test_library_output_path = os.path.realpath(os.path.join(p.TEMP_PROJECT_PATH, p.LIBRARY_DIR_NAME))
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
            os.remove(os.path.join(test_library_output_path, "setup.py"))
            os.remove(os.path.join(test_library_output_path, "setup.pyc"))
            os.remove(os.path.join(test_library_output_path, "__init__.pyc"))
            shutil.rmtree(os.path.join(test_library_output_path, "plugins"))
        except Exception as e:
            None

        try:
            shutil.copy2(test_plugin_setup_file, test_library_output_path)
            copy_tree(test_plugins, test_plugins_output_path)
            print("Copied: ")
            print(test_plugin_setup_file + " -> " + test_library_output_path)
            print(test_plugins + " -> " + test_plugins_output_path)
        except Exception as e:
            print("ERROR: Failed to copy files")
            print(str(e))
            result = rc.FAIL

    os.chdir(start_directory)
    print("Changed directory to " + str(start_directory))

    return (result)

def run_and_check(cmd, expected):
    result = rc.PASS
    shell_return = f.shell_run(cmd)
    if shell_return[0] != 0:
        print("[ERROR]: Failed to run command: " + str(cmd))
        result = rc.FAIL

    if result == rc.PASS:
        for exp in expected:
            if exp not in shell_return[1]:
                print("[ERROR]: Unexpected command error. Expected '" + str(expected) + "'. Got '" +
                      str(shell_return[1]) + "'")
                result = rc.FAIL

    return result

def test_command_hook(task):
    result = rc.PASS
    start_dir = os.getcwd()
    # Navigate to temp project dir and run
    try:
        os.chdir(p.TEMP_PROJECT_PATH)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + p.TEMP_PROJECT_PATH + "'")

    # Rename target setup file to "setup.py"
    if result == rc.PASS:
        print("Changed directory to " + str(p.TEMP_PROJECT_PATH))

        result = run_and_check("krem test", ["Running test command"])

    try:
        os.chdir(start_dir)
    except Exception:
        if result == rc.PASS:
            result = rc.UNSTABLE
        print("ERROR: Failed to return to start directory.")

    return result

def test_argument_setup_hooks(task):
    result = rc.PASS
    start_dir = os.getcwd()

    # Navigate to temp project dir and run
    try:
        os.chdir(p.TEMP_PROJECT_PATH)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + p.TEMP_PROJECT_PATH + "'")

    # Rename target setup file to "setup.py"
    if result == rc.PASS:
        print("Changed directory to " + str(p.TEMP_PROJECT_PATH))

        init_result = run_and_check("krem init --help", ["test command help string"])
        run_result = run_and_check("krem run --help", ["test command help string"])
        list_result = run_and_check("krem list --help", ["test command help string"])
        
        if init_result or run_result or list_result:
            result = rc.FAIL

    try:
        os.chdir(start_dir)
    except Exception:
        if result == rc.PASS:
            result = rc.UNSTABLE
        print("ERROR: Failed to return to start directory.")

    return result

def test_argument_execute_hooks(task):
    result = rc.PASS
    start_dir = os.getcwd()

    # Navigate to temp project dir and run
    try:
        os.chdir(p.TEMP_PROJECT_PATH)
    except Exception:
        result = rc.FAIL
        print("ERROR: Failed to change current directory to: '" + p.TEMP_PROJECT_PATH + "'")

    # Rename target setup file to "setup.py"
    if result == rc.PASS:
        print("Changed directory to " + str(p.TEMP_PROJECT_PATH))

        init_result = run_and_check("krem init -x", ["Executing pre_cmd hook", "Received argument in pre_cmd", "Executing post_cmd hook", "Received argument in post_cmd"])
        run_result = run_and_check("krem run -x", ["Executing pre_cmd hook", "Received argument in pre_cmd", "Executing post_cmd hook", "Received argument in post_cmd"])
        list_result = run_and_check("krem list -x", ["Executing pre_cmd hook", "Received argument in pre_cmd", "Executing post_cmd hook", "Received argument in post_cmd"])
            
        if init_result or run_result or list_result:
            result = rc.FAIL

    try:
        os.chdir(start_dir)
    except Exception:
        if result == rc.PASS:
            result = rc.UNSTABLE
        print("ERROR: Failed to return to start directory.")

    return result



