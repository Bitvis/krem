#!/usr/bin/env python
## \file run.py
## \brief Executes target job/task

'''
# Copyright (C) 2017  Bitvis AS
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
import os
import subprocess
import sys
import re
import shutil

from krempack.common import kremtree
from krempack.common import constants as c
from krempack.core.commands import init
from krempack.core.commands import list

def check_if_job_number(target):
    num = 0
    if isinstance(target, int):
        num = target
    elif isinstance(target, str) and target.isdigit():
        num = int(target)
    else:
        num = -1
        
    return num

# Run job file
def run_job(target):
    ret = 0
    err = False
    jobs_path = kremtree.find_common_dir(c.PROJECT_JOBS_DIR)
    
    idx = 0
    job_num = check_if_job_number(target)
    
    if not job_num < 0:
        jobs = kremtree.list_dir(jobs_path)
        if not job_num + 1 > len(jobs):
            for job in jobs:
                if idx == job_num:
                    print("running job: " + str(job))
                    target = job
                    break
                idx = idx + 1

        else:
            print("Invalid job number: " + str(job_num))
            err = True
            
    if not err:
        #this will add project path to sys path so jobs can acces library, config, etc
        current_env = os.environ.copy()
        current_env['PYTHONPATH'] += ':'.join("/.")
        
        target_path = os.path.join(jobs_path, target, c.TEMPLATE_JOB_SCRIPT)
        try:
            ret = subprocess.call(['python', target_path], env=current_env)
        except Exception as e:
            print("Invalid job: " + str(target))
        
    return ret
    
# Creates job file by using template job
# TODO: Rewrite for new version of KREM (unused in v1.0.0)
def create_job(target, tasks=[]):
    init.deploy_template(c.TEMPLATE_JOB, target)
    job_path = os.path.join(os.path.abspath(kremtree.find_common_dir(c.PROJECT_JOBS_DIR)), target)
    job_file = os.path.join(job_path, c.TEMPLATE_JOB_SCRIPT)
    
    f = open(job_file, 'r')
    contents = f.readlines()
    f.close()
    
    index = 0
    for idx, line in enumerate(contents):
        if re.match('.*Add tasks here', line) is not None:
            index = idx + 1
    
    for idx, task in enumerate(tasks):
        contents.insert(index + idx, task)
        
    f = open(job_file, 'w')
    for line in contents:
        f.write(line)
    f.close()
    
    return job_path

# Creates temporary job based on list of calls to 'add_task()'
# The job is executed, then removed
#TODO: Rewrite for new version of KREM (unused in v1.0.0)
def run_temporary_job(name, call_list):
    job_path = create_job(name, call_list)
    ret = run_job(name)
    print('Removing temporary job: ' + str(name))
    shutil.rmtree(job_path)
    print(ret)
    return ret

# Creates list of calls to 'add_task()' with
# input tasks and an action (run)
#TODO: Rewrite for new version of KREM (unused in v1.0.0)
def build_call_list(tasks = []):
    call_list = []
    
    for i, task in enumerate(tasks):
        call_list.append("    job.add_task('" + str(task) + "', " + str(i + 1) + ")\n")
        
    return call_list

# Runs list of tasks with specified action
def run_tasks(job_name, tasks = []):
    call_list = build_call_list(tasks)
    return run_temporary_job(job_name, call_list)

# Runs all tasks with specified action
def run_all_tasks(job_name):
    tasks_path = kremtree.find_common_dir(c.PROJECT_TASKS_DIR)
    if tasks_path is not None:
        tasks_path = os.path.abspath(tasks_path)
        tasks = kremlist.list_dir(tasks_path)
        return run_tasks(job_name, tasks)
    return 1


        
        
        
