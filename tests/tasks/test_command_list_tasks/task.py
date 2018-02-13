#!/bin/env python
import sys
import os
import subprocess
import re

from library.returncodes import *
from library.testlib import parameters as p
from library.testlib import functions as f


def run(task):

    result = rc.PASS

    tasks_in_dir = []
    listed_tasks = []
    missing_from_list = []
    missing_from_tasks_dir = []
    
    shell_return = f.shell_run("krem list " + p.CMD_LIST_OPTION_TASK)
    if shell_return[0] != 0:
        result = rc.FAIL
    
    if not result:
        # Get list of tasks
        print("tasks listed:")
        
        taskprint = re.findall(p.LIST_ID_REGEX + '.*', shell_return[1])
        for task in taskprint:
            m = re.search(p.LIST_ID_REGEX, task)
            if m:
                task = task.replace(m.group(), '')
                task = task.strip()
                listed_tasks.append(task)
                print(task)

        # Get tasks in task directory
        tasks_dir = os.listdir(p.TEST_PROJECT_TASKS_DIR) 
        print("\nTasks present in tasks directory:")        
        for task in tasks_dir:
            if os.path.isdir(os.path.join(p.TEST_PROJECT_TASKS_DIR, task)):
                print(task)
                tasks_in_dir.append(task)

    # compile results
    if not result:
        missing_from_list = f.compare_lists(listed_tasks, tasks_in_dir)
        missing_from_tasks_dir = f.compare_lists(tasks_in_dir, listed_tasks)
        
        if len(missing_from_list) > 0:
            print("\nERROR: Files present in tasks dir that was not listed: " + str(missing_from_list))
            result = rc.FAIL
        if len(missing_from_tasks_dir):
            print("\nERROR: Files listed that are not present in tasks dir: " + str(missing_from_tasks_dir))
            result = rc.FAIL


    return(result)


