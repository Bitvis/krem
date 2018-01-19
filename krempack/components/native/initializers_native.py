
## \file initializers_native.py
## \brief Default implementation of Initializer classes 

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

import time
import os, os.path
import sys
import shutil

from krempack.components import initializers
from krempack.core import ktask

from krempack.common import constants as c
from krempack.common import kremtree

import difflib
import string
import re

#######################################
#   Default job initializer. Sets up
#       output directory for job.
#   NOTE: Do not use logger in this class,
#   as the logger will most likely be setup
#   to place logfile in output directory which
#   is not created yet
#######################################
class JobInitializerNative(initializers.JobInitializer):
    
    def execute(self, target):
        instance_output_name = self.time_stamp()
        output_path = kremtree.find_common_dir(c.PROJECT_OUTPUT_DIR)
        job_output_path = os.path.join(output_path, target)
        instance_output_path = os.path.join(job_output_path, instance_output_name)
        
        # Create job output directory
        if not os.path.isdir(job_output_path):
            try:
                os.mkdir(job_output_path)
                print("\n\nJob output initialized in directory " + job_output_path + '\n')
            except Exception as e:
                print("[INTERNAL_ERROR]: Unable to create " + job_output_path)
                exit(1)            
        
        # Create instance output directory
        try:
            os.mkdir(instance_output_path)
            print("\n\nJob instance output initialized in directory " + instance_output_path + '\n')
        except Exception as e:
            print("[INTERNAL_ERROR]: Unable to create " + instance_output_path)
            exit(1)
          
        # Create global info file in output directory
        try:
            info_path = os.path.join(output_path, c.INFO_FILE)
            f = open(info_path, 'w')
            f.write('LAST_JOB = ' + str(target) + '/' + str(instance_output_name) + '\n')
            f.close()            
              
        except:
            print("[INTERNAL_WARNING]: Unable to create file " + info_path)
            
        # Add project path to syspath
        projectPath = os.path.join(kremtree.find_krem_root('./'))
        projectPath = os.path.realpath(projectPath)
        sys.path.append(projectPath)
            
        
        self.rotateSubdirs( job_output_path, '\d+_\d+', c.PROJECT_KEEP_OUTPUT_DIRS )
        
            
        return instance_output_path
        
    def time_stamp(self):
        return time.strftime("%Y%m%d_%H%M%S", time.localtime())
    
    

    def rotateSubdirs( self, path, pattern, keepDirs ):
        #remove oldest dirs for given job
        
        path = path + '/'
        
        allDirs = os.listdir(path)
      
        dirCount = 0
        dirs = []
        
        #find all dirs matching pattern
        for subdir in allDirs:
            if os.path.isdir(path + subdir):      
                match = re.findall(pattern, subdir)
                if match:
                    dirCount += 1
                    dirs.append(subdir)
                
        #sort so we get the oldest first in list        
        dirs.sort() 
        
        #remove oldest dirs up to keepDirs
        while (dirCount > keepDirs):
            dirCount -= 1
            shutil.rmtree(path + dirs[0])
            del dirs[0]
            
        #set latest dir link
        latestLinkPath = os.path.join(path, 'latest')
        if (dirCount > 0):
            latestDir = dirs[len(dirs)-1]
            #create link to latest dir
            if os.path.islink(latestLinkPath):
                os.remove(latestLinkPath)
            os.symlink(latestDir, latestLinkPath)
        
        return;

        
    
    
#########################################
#   Default task initializer.
#       Sets up output directory for
#       each task
#########################################
class TaskInitializerNative(initializers.TaskInitializer):
    
    def execute(self, target):
        
        target.set_output_path(os.path.abspath(os.path.join(target.config.get_root_output_path(), target.get_task_name())))
        
        
        # Create output directory for this task
        try:
            os.mkdir(target.get_output_path())
            self.log.write("Task initialized: " + target.get_output_path(), 'debug')
        except:
            self.log.write("Unable to create output directory for task: " + target.get_output_path(), 'error')

    # Task name = <run_nr>_<task_name>__<action>_<parallel_nr?>
    def generate_task_name(self, new_task, task_list=[]):
        module_name = new_task.get_target_module_name()
        
        if module_name is not None:
            module_name = module_name.split('.')[1]

            task_name = str(new_task.get_run_nr()) + '_' + new_task.get_target() + '__' + str(new_task.get_target_function())

            # Append postfix number. Used for identifying append order for parallel tasks
            num_task = 0
            for task in task_list:
                if task.run_nr is new_task.run_nr:
                    num_task = num_task + 1

            task_name = task_name + '_' + str(num_task)


            new_task.set_task_name(task_name)
        
    def compile_task_module_name_and_path(self, task):
        setup_file_path = os.path.join(kremtree.find_common_dir(c.PROJECT_TASKS_DIR), task.get_target(), c.TEMPLATE_TASK_SETUP_FILE)
        param = None
        param_split = None
        path = None
        module_name = None
        
        # Search for path in setup file
        f = open(setup_file_path)
        for line in f.readlines():
            param = re.findall(c.TEMPLATE_TASK_SETUP_PARAM_NAME_SCRIPT_PATH, line)
            
            if len(param) > 0:
                param_split = line.rsplit('=')
                if len(param_split) >= 2:
                    path = param_split[1].strip()
                    path = path.rstrip('\n\r')
                    
                    module_name = os.path.basename(path)
                    module_name = module_name.strip('.py')
                    module_name = task.get_target() + '.' + module_name
                    break
                    
        # Check if path exists
        if path is not None:
            if path[:2] is './':
                path.rstrip('./')
                path = os.path.join(kremtree.find_common_dir(c.PROJECT_TASKS_DIR), task.get_target(), path)
            elif path[:1] is '/':
                pass
            else:
                slashes = re.findall('//', path)
                if not len(slashes) > 0:
                    path = os.path.join(kremtree.find_common_dir(c.PROJECT_TASKS_DIR), task.get_target(), path)
            
            if not os.path.isfile(path):
                path = None
        else:
            self.log.write("Path to task not found in setup file", 'error')
                    
        if path is not None and module_name is not None:
            task.set_target_module_name(module_name)
            task.set_target_module_path(path)
        else:
            self.log.write("Path to module in task: " + str(task.get_target()) + " not found in setup file", 'error')
            self.log.write("Ensure setup.txt exists in task folder, and correct name/path is given", 'error')
            exit(1)
            
