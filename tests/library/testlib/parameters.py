#!/bin/env python
import os
from krempack.common import constants as c

# Test items
SIMPLE_TASK = "simple_task"
SIMPLE_JOB = "simple_job"

test_var_list = ["foo", "bar"]
test_var_1 = "foo"
test_var_2 = "bar"

#Regex
LIST_ID_REGEX = '\[\d+\]'
TIMESTAMP_REGEX = '^\d+_\d+'

#Paths
#EXPECTED_PROJECT_DIRECTORIES = c.PROJECT_DEFAULT_DIRS
TEST_PROJECT_LIBRARY_PATH = os.path.dirname(os.path.realpath(__file__))

TEST_PROJECT_ROOT_PATH = os.path.realpath(os.path.join(TEST_PROJECT_LIBRARY_PATH, "..",".."))

CONFIG_DIR_NAME = "config"
LIBRARY_DIR_NAME = "library"

JOBS_DIR_NAME = "jobs"
TEST_PROJECT_JOBS_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, JOBS_DIR_NAME)

TASKS_DIR_NAME = "tasks"
TEST_PROJECT_TASKS_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, TASKS_DIR_NAME)

OUTPUT_DIR_NAME = "output"
TEST_PROJECT_OUTPUT_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, OUTPUT_DIR_NAME)

OUTPUT_LATEST_SYMLINK = "latest"

TEMP_PROJECT_NAME = "krem_temp"
TEMP_PROJECT_PATH = os.path.join(TEST_PROJECT_ROOT_PATH, "..", TEMP_PROJECT_NAME)

TEMP_JOB_NAME = "temp_job"
DEAFULT_JOB_SCRIPT = "job.py"

TEMP_TASK_NAME = "temp_task"
DEAFULT_TASK_SCRIPT = "run.py"
DEAFULT_TASK_SETUP_FILE = "setup.txt"


#Commands and options
CMD_LIST = "list"
CMD_LIST_OPTION_TASK = '-t'
CMD_LIST_OPTION_JOB = '-j'

CMD_INIT = "init"
CMD_INIT_OPTION_PROJECT = '-p'
CMD_INIT_OPTION_JOB = '-j'
CMD_INIT_OPTION_TASK = '-t'

CMD_RUN = "run"
CMD_RUN_OPTION_JOB = "-j"

# Expected output
EXPECTED_OUTPUT_JOB_INSTANCE_DIR = os.path.join(SIMPLE_JOB, "job_instance")
EXPECTED_OUTPUT_JOB_DIR = os.path.join(SIMPLE_JOB, "job_instance", "1_" + SIMPLE_TASK + "__run_1") # Must replace "job_instance" with actual job instance name in task (common function: find_output_job_instance() 
EXPECTED_OUTPUT_DIRS = [SIMPLE_JOB, EXPECTED_OUTPUT_JOB_INSTANCE_DIR, EXPECTED_OUTPUT_JOB_DIR]
EXPECTED_OUTPUT_FILE_RUN_LOG = os.path.join(EXPECTED_OUTPUT_JOB_INSTANCE_DIR, "run.txt")
EXPECTED_OUTPUT_FILE_RESULTS = os.path.join(EXPECTED_OUTPUT_JOB_INSTANCE_DIR, "results.txt")
EXPECTED_OUTPUT_FILE_TASK_LOG = os.path.join(EXPECTED_OUTPUT_JOB_INSTANCE_DIR, "tasks.log")

# Expected file contents
EXPECTED_CONTENT_RUN_LOG = ["[INFO]: Execute task:",
                            "[INFO]: Results written to:"]
EXPECTED_CONTENT_TASK_LOG = ["This is just a simple task"]

EXPECTED_CONTENT_RESULTS = ["TASK                                     RESULT",
                            "1_simple_task__run_1                     PASS",
                            "2_simple_task__run_1                     PASS",
                            "3_simple_task__run_1                     PASS",
                            "4_simple_task__run_1                     PASS",
                            "5_simple_task__run_1                     PASS",
                            "6_simple_task__run_1                     PASS",
                            "7_simple_task__run_1                     PASS",
                            "8_simple_task__run_1                     PASS",
                            "9_simple_task__run_1                     PASS",
                            "10_simple_task__run_1                    PASS",
                            "11_simple_task__run_1                    PASS",

                            "SUMMARY:",

                            "PASS                 11",
                            "FAIL                 0",
                            "SKIP                 0",
                            "UNSTABLE             0",]



