
## \file run.py
## \brief Executes target job/task

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

    jobs_path = kremtree.find_common_dir(c.PROJECT_JOBS_DIR)
    
    if not os.path.isdir(os.path.join(kremtree.find_krem_root("./"), c.PROJECT_OUTPUT_DIR)):        
        templatePath = os.path.join(c.TEMPLATES_PATH, c.TEMPLATE_PROJECT)
        shutil.copytree(os.path.join(templatePath, c.PROJECT_OUTPUT_DIR), os.path.join(kremtree.find_krem_root("./"), c.PROJECT_OUTPUT_DIR))
    
    idx = 0
    job_num = check_if_job_number(target)
    
    if job_num >= 0:
        jobs = kremtree.list_dir(jobs_path)
        jobs.sort()
        if not job_num + 1 > len(jobs):
            for job in jobs:
                if idx == job_num:
                    print("\nRunning job: " + str(job) +"\n")
                    target = job
                    break
                idx = idx + 1                
        else:
            print("Invalid job number: " + str(job_num))   
            ret = 1         

    if ret == 0:
        target_path = os.path.join(jobs_path, target, c.TEMPLATE_JOB_SCRIPT)
        if not os.path.exists(target_path):
            print("Invalid job: " + str(target)) 
            ret = 1


    if ret == 0:
        #this will add project path to sys path so jobs can acces library, config, etc
        current_env = os.environ.copy()
        current_env['PYTHONPATH'] += os.pathsep + os.path.join(os.path.dirname("."))

        if os.stat(target_path).st_size == 0:
            print("[ERROR]: Target job-script is empty.")
            exit(1)

        try:
            ret = subprocess.call(['python', target_path], env=current_env)
        except Exception:
            print("Invalid job: " + str(target))
            ret = 1        

    return ret
