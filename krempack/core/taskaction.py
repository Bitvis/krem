
## \file ktask_native.py
## \brief Default implementation of TaskAction class

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
from subprocess import Popen, PIPE, STDOUT
import sys
import pickle
from importlib import import_module
import re

from krempack.core import executor
from krempack.core import ktask

from krempack.common import constants as c
from krempack.common import kremtree


## Default task action
#
# Executes target function in target task module
class TaskAction():
    name = 'default'
    log = None
   
    ## Constructor 
    def __init__(self):
        self.script_path = None
        self.task = None
        
    def set_target_task(self, task):
        self.task = task
        
    def set_logger(self, logger):
        self.log = logger    
        
    def get_name(self):
        return self.name

    ## Executes target function to target task module
    def run_method(self, queue):
        module_path = None
        target_function = None
        setup_task = None
        target_method = None 
        returncode = 1
        var_dict = {}
        var_list = []
        taskVars = self.task.get_variables()
        
        self.task.initialize()
        
        setup_task = self.get_setup_task_function()
        if setup_task is not None:
            task_data = ktask.TaskData()
            task_data.set_task_name(self.task.get_task_name())
            task_data.set_run_nr(self.task.get_run_nr())
            task_data.set_job_path(self.task.get_job_path())
            task_data.set_path(self.task.get_path())
            task_data.set_output_path(self.task.get_output_path())
            setup_task(task_data)
        
        self.log.write("Execute task: " + self.task.get_task_name(), 'info') 
        
        os.environ = self.task.get_environ()
        
        if len(taskVars) > 0:
            for var in taskVars:
                if isinstance(var, tuple) and len(var) == 2:
                    var_dict[var[0]] = var[1]
                elif not isinstance(var, list) and not isinstance(var, dict):
                    var_list.append(var)
                 
        
        stdout_saveout = sys.stdout
        stderr_saveout = sys.stderr
        
        try:
            target_function = self.get_function_to_run()

            if target_function is not None:
                self.task.get_logger().enable(self.task)

                self.task.plugin_handler.entrypoints["pre_task_function_call"].execute({"task":self.task})
                
                if len(var_dict) > 0 and len(var_list) > 0:
                    returncode = target_function(var_list, **var_dict)
                elif len(var_dict) > 0:
                    returncode = target_function(**var_dict)
                elif len(var_list) > 0:
                    returncode = target_function(var_list)
                else:
                    returncode = target_function()
        
                self.task.set_task_result(returncode)            
                self.task.plugin_handler.entrypoints["post_task_function_call"].execute({"task":self.task})

                self.task.get_logger().disable(self.task)
        except Exception as e:
            sys.stdout = stdout_saveout
            sys.stderr = stderr_saveout
            self.log.write(str(sys.exc_info()[0]) + ' : ' + str(e), 'error')
          
            
        self.log.write(self.task.get_task_name() + " return code: " + str(self.task.get_task_result()), 'debug')
        
        queue.put({self.task.get_task_name():self.task})
        
    ## Retreive target function from target task module
    #  @return Target function 
    def get_function_to_run(self):
        path = None
        module = None
        module_name = None
        function = None
        
        module_name = self.task.get_target_module_name()
        module_path = self.task.get_target_module_path()
        
        if module_path is not None and module_name is not None:
            module_path = os.path.dirname(os.path.realpath(module_path)) + '/../'
            sys.path.append(module_path)
            module = import_module(module_name)
            
        if module is not None:
            try:
                function = getattr(module, self.task.get_target_function())
            except:
                self.log.write("function '" + str(self.task.get_target_function()) + "' in task '" + str(self.task.get_task_name()) + "' not found", 'error')
            
        return function
            
            
    ## Retreive setup task function from target task module
    #  @return Setup task function 
    def get_setup_task_function(self):
        path = None
        module = None
        module_name = None
        function_name = "setup_task"
        function = None
        
        module_name = self.task.get_target_module_name()
        module_path = self.task.get_target_module_path()
        
        if module_path is not None and module_name is not None:
            module_path = os.path.dirname(os.path.realpath(module_path)) + '/../'
            sys.path.append(module_path)
            module = import_module(module_name)
            
        if module is not None:
            try:
                function = getattr(module, function_name)
                self.log.write("function '" + function_name + "' in task '" + str(self.task.get_task_name()) + "' executing", 'info')
            except:
                #be silent, it is not an error if the function is missing as it is optional
                pass 
        return function                   
                
            
            
            

