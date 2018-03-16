
## \file initializers_native.py
## \brief Default implementation of Initializer classes 

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
import platform

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
        output_path = os.path.abspath(kremtree.find_common_dir(c.PROJECT_OUTPUT_DIR))
        job_output_path = os.path.join(output_path, target)
        instance_output_path = os.path.join(job_output_path, instance_output_name)
        
        # Create job output directory
        if not os.path.isdir(job_output_path):
            try:
                os.mkdir(job_output_path)
            except Exception as e:
                print("[INTERNAL_ERROR]: Unable to create " + job_output_path)
                exit(1)            
        
        # Create instance output directory
        try:
            os.mkdir(instance_output_path)

        except Exception:
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
            
        self.rotateSubdirs( job_output_path, '\d+_\d+', c.PROJECT_KEEP_OUTPUT_DIRS )
        
        return instance_output_path
        
    def time_stamp(self):
        return time.strftime("%Y%m%d_%H%M%S", time.localtime())
    
    

    def rotateSubdirs( self, path, pattern, keepDirs ):
        #remove oldest dirs for given job
       
        allDirs = os.listdir(path)
      
        dirCount = 0
        dirs = []
        
        #find all dirs matching pattern
        for subdir in allDirs:
            if os.path.isdir(os.path.join(path, subdir)):      
                match = re.findall(pattern, subdir)
                if match:
                    dirCount += 1
                    dirs.append(subdir)
                
        #sort so we get the oldest first in list        
        dirs.sort() 
        
        #remove oldest dirs up to keepDirs
        while (dirCount > keepDirs):
            dirCount -= 1
            shutil.rmtree(os.path.join(path, dirs[0]))
            del dirs[0]
       
        try:  #Move up if current directory doesn't exist
            os.getcwd()
        except Exception:
            os.chdir("..")

     
        #set latest dir link
        latestLinkPath = os.path.join(path, 'latest')
        if (dirCount > 0):
            latestDir = dirs[len(dirs)-1]
            #create link to latest dir
            #links are not supported on Linux
            if platform.system() == 'Linux':
                if os.path.islink(latestLinkPath):
                    os.remove(latestLinkPath)
                os.symlink(latestDir, latestLinkPath)
        
        return

        
    
    
#########################################
#   Default task initializer.
#       Sets up output directory for
#       each task
#########################################
class TaskInitializerNative(initializers.TaskInitializer):
    
    def execute(self, target):
        
        target.set_output_path(os.path.abspath(os.path.join(target.config.get_root_output_path(), target.get_run_name())))
        
        
        # Create output directory for this task
        try:
            os.mkdir(target.get_output_path())
            self.log.write("Created output directory: " + target.get_output_path(), 'debug')
        except:
            self.log.write("Unable to create output directory for task: " + target.get_output_path(), 'error')

    # Task name = <run_nr>_<task_name>__<action>_<parallel_nr?>
    def generate_run_name(self, new_task, task_list=[]):
        module_name = new_task.get_target_module_name()
        
        if module_name is not None:
            module_name = module_name.split('.')[1]

            # Append postfix number. Used for identifying append order for parallel tasks
            num_task = 0
            for task in task_list:
                if task.run_nr is new_task.run_nr:
                    num_task = num_task + 1

            task_name = str(new_task.get_run_nr()) + '_' + str(num_task) + '_' + new_task.get_target() +'_'+ str(new_task.get_target_function()) +''

            new_task.set_full_run_nr(str(new_task.get_run_nr()) + '_' + str(num_task))
            new_task.set_run_name(task_name)
        
    def compile_task_module_name_and_path(self, task):
        task_path = None
        module_name = None

        task_path = os.path.join(kremtree.find_common_dir(c.PROJECT_TASKS_DIR), task.get_target(), c.TEMPLATE_TASK_FILE)

        if not os.path.isfile(task_path):
            self.log.write("Path to module in task: " + str(task.get_target()) + " not found in task.cfg file", 'error')
            self.log.write("Ensure task.cfg exists in task folder, and correct name/path is given", 'error')
            exit(1)

        module_name = c.TEMPLATE_TASK_FILE
        module_name = module_name.strip('.py')
        module_name = task.get_target() + '.' + module_name

        task.set_target_module_name(module_name)
        task.set_target_module_path(task_path)






