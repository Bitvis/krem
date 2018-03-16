
## \file kremlist.py
## \brief Listing tasks in jon, available taks and available jobs

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
import sys
import re

from krempack.common import kremtree
from krempack.common import constants as c


            
# Get all jobs in 'jobs' dir
def list_jobs():
    jobs_path = os.path.abspath(kremtree.find_common_dir(c.PROJECT_JOBS_DIR))
    job_list = kremtree.list_dir(jobs_path)
    job_list.sort()

    print("\nAvailable jobs: \n")
    print("[nr]\tname\n")
    idx = 0
    for job in job_list:
        print("[" + str(idx) + "]\t" + str(job))
        idx = idx + 1
    print('\n')
    
# Get all tasks in 'tasks' dir
def list_tasks():
    tasks_path = kremtree.find_common_dir(c.PROJECT_TASKS_DIR)
    if tasks_path is not None:
        tasks_path = os.path.abspath(tasks_path)
        tasks_list = kremtree.list_dir(tasks_path)
        tasks_list.sort()

        print("\nAvailable tasks:\n")
        print("[nr]\tname\n")

        idx = 0
        for task in tasks_list:
            missingFiles = []
            printstring = "[" + str(idx) + "]\t" + str(task)
            # List scripts in task, to quickly see if something is missing
            task_path = os.path.join(tasks_path, task)

            if not os.path.isfile(os.path.join(task_path, c.TEMPLATE_TASK_FILE)):
                missingFiles.append(c.TEMPLATE_TASK_FILE)
            if not os.path.isfile(os.path.join(task_path, c.INIT_PACKAGE_FILE)):
                missingFiles.append(c.INIT_PACKAGE_FILE)
                    
            if len(missingFiles) > 0:
                printstring = printstring + '\t' + "missing files: " + str(missingFiles)

            print(printstring)
            idx = idx + 1
        print("")
        

            
    
                                    
                                    

