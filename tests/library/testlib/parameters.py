#!/bin/env python
import os
from krempack.common import constants as c

# Test items
SIMPLE_TASK = "simple_task"
SIMPLE_JOB = "simple_job"

test_arg_list = ["foo", "bar"]
test_arg_1 = "foo"
test_arg_2 = "bar"
test_arg_dict = {'a': 1, 'b': 2, 'c': 3}
test_arg_int = 5
test_arg_float = 6.5

#Regex
LIST_ID_REGEX = '\[\d+\]'
TIMESTAMP_REGEX = '^\d+_\d+'

#Paths
#EXPECTED_PROJECT_DIRECTORIES = c.PROJECT_DEFAULT_DIRS
TEST_PROJECT_LIBRARY_PATH = os.path.dirname(os.path.realpath(__file__))

TEST_PROJECT_ROOT_PATH = os.path.realpath(os.path.join(TEST_PROJECT_LIBRARY_PATH, "..",".."))

KREM_PATH = os.path.realpath(os.path.join(TEST_PROJECT_ROOT_PATH, ".."))

KREM_CMD = "python " + KREM_PATH + "/krem "

CONFIG_DIR_NAME = "config"
LIBRARY_DIR_NAME = "library"

JOBS_DIR_NAME = "jobs"
TEST_PROJECT_JOBS_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, JOBS_DIR_NAME)

TASKS_DIR_NAME = "tasks"
TEST_PROJECT_TASKS_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, TASKS_DIR_NAME)

OUTPUT_DIR_NAME = "output"
TEST_PROJECT_OUTPUT_DIR = os.path.join(TEST_PROJECT_ROOT_PATH, OUTPUT_DIR_NAME)

OUTPUT_LATEST_SYMLINK = "latest"

TEMP_PROJECT_NAME = "temp_krem"
TEMP_PROJECT_PATH = os.path.join(TEST_PROJECT_ROOT_PATH, OUTPUT_DIR_NAME, TEMP_PROJECT_NAME)

TEMP_JOB_NAME = "temp_job"
JOB_SCRIPT = "job.py"

TEMP_TASK_NAME = "temp_task"
TASK_SCRIPT = "task.py"


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
EXPECTED_OUTPUT_JOB_DIR = os.path.join(SIMPLE_JOB, "job_instance", "1_1_" + SIMPLE_TASK + "_run") # Must replace "job_instance" with actual job instance name in task (common function: find_output_job_instance()
EXPECTED_OUTPUT_DIRS = [SIMPLE_JOB, EXPECTED_OUTPUT_JOB_INSTANCE_DIR, EXPECTED_OUTPUT_JOB_DIR]
EXPECTED_OUTPUT_FILE_EXECUTION_LOG = os.path.join(EXPECTED_OUTPUT_JOB_INSTANCE_DIR, "execution.log")
EXPECTED_OUTPUT_FILE_RESULTS = os.path.join(EXPECTED_OUTPUT_JOB_INSTANCE_DIR, "results")
EXPECTED_OUTPUT_FILE_TASK_LOG = os.path.join(EXPECTED_OUTPUT_JOB_INSTANCE_DIR, "tasks.log")

# Expected file contents
EXPECTED_CONTENT_EXECUTION_LOG = ["[INFO]: 1_1", "simple_task", "run",
                            "[INFO]: Results written to:"]
EXPECTED_CONTENT_TASK_LOG = ["This is just a simple task"]

EXPECTED_CONTENT_RESULTS = ["        TASK          FUNCTION RESULT",
"1_1","simple_task","run","PASS",
"2_1","simple_task","run","PASS",
"2_2","simple_task","run","PASS",
"2_3","simple_task","run","PASS",
"2_4","simple_task","run","PASS",
"2_5","simple_task","run","PASS",
"2_6","simple_task","run","PASS",
"2_7","simple_task","run","PASS",
"2_8","simple_task","run","PASS",
"2_9","simple_task","run","PASS",
"2_10","simple_task","run","PASS",

"SUMMARY:",

"ERROR                0",
"EXCEPTION            0",
"FAIL                 0",
"PASS                 11",
"SKIPPED              0",
"SUCCESS              0",
"UNSTABLE             0",]



