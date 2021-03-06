## \file constants.py
## \brief Global constants

'''
# Copyright (C) 2018  Bitvis AS
#
# This file is part of KREM.
#
# KREM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KREM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with KREM.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Bitvis AS 
# www.bitvis.no
# info@bitvis.no
'''

'''
description:
	Contains global constants for this package.
	To use constants, import this module using
	'import kremConstants as c', and call constants
	'c.KREM_PATH'
'''

import os


# Paths and files
KREM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

TEMPLATES_PATH = os.path.join(KREM_PATH, 'krempack', 'templates')

TEMPLATE_PROJECT = "project"
TEMPLATE_TASK = "task"
TEMPLATE_JOB = "job"

TEMPLATE_TASK_FILE = "task.py"
TEMPLATE_JOB_SCRIPT = "job.py"

TASK_FILE = "task.py"
INIT_PACKAGE_FILE = "__init__.py"

PROJECT_CONFIG_DIR = "config"
PROJECT_LIB_DIR = "library"
PROJECT_TASKS_DIR = "tasks"
PROJECT_JOBS_DIR = "jobs"
PROJECT_OUTPUT_DIR = "output"
PROJECT_KEEP_OUTPUT_DIRS = 5
PROJECT_DEFAULT_DIRS = [PROJECT_CONFIG_DIR, PROJECT_LIB_DIR, PROJECT_TASKS_DIR, PROJECT_JOBS_DIR]

TASK_LOG = "task.log"
INFO_FILE = "info"

# Plugin info
runtime_hooks = ["pre_job_start", "job_start", "pre_task_execution", "job_progress_text", "pre_task_function_call", "post_task_function_call", "post_task_execution", "job_end"]
cli_hooks = ["cli_commands", "cli_init_setup_arguments", "cli_init_execute_arguments_pre_cmd", "cli_init_execute_arguments_post_cmd",
             "cli_run_setup_arguments", "cli_run_execute_arguments_pre_cmd", "cli_run_execute_arguments_post_cmd",
             "cli_list_setup_arguments", "cli_list_execute_arguments_pre_cmd", "cli_list_execute_arguments_post_cmd"]
