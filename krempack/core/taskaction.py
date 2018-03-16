
## \file ktask_native.py
## \brief Default implementation of TaskAction class

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
from subprocess import Popen, PIPE, STDOUT
import sys
import pickle
from importlib import import_module
import re

from krempack.core import executor
from krempack.core import ktask
from krempack.common import constants as c
from krempack.common import kremtree
from library.returncodes import *
from library.colorcodes import *
import traceback


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
        target_function = None
        returncode = 1
        arg_dict = {}
        arg_list = []
        arg_single = None
        taskArgs = self.task.get_arguments()
        
        self.task.initialize()

        module = self.import_task_module()

        progress = []
        progress.append('{0:8}{1}{2}'.format(self.task.get_full_run_nr(), cc.WHITE, self.task.get_task_name()))
        progress.append("  " + cc.YELLOW + self.task.get_target_function() + cc.RESET)
        progress.append("  " + cc.GRAY + str(self.task.get_arguments()) + cc.RESET)

        #this hook will allow plugins to modify progress text
        self.task.plugin_handler.execute_hook("job_progress_text", {"task": self.task, "progress_text": progress})

        self.log.write(" ".join(progress), 'info')

        self.task.get_logger().enable(self.task)

        # we cannot check length of int and float so we check the type for those
        # before we check for length
        if type(taskArgs) == int or type(taskArgs) == float:
            arg_single = taskArgs
        else:

            if len(taskArgs) > 0:
                if type(taskArgs) == dict:
                    arg_dict = taskArgs
                if type(taskArgs) is not list:
                   arg_single = taskArgs
                else:
                    for arg in taskArgs:
                        if type(arg) == tuple and len(arg) == 2:
                            arg_dict[arg[0]] = arg[1]
                        elif not type(arg) == list and not type(arg) == dict:
                            arg_list.append(arg)

        try:

            target_function = self.get_function_to_run(module)

            if target_function is not None:

                task_data = ktask.TaskData()
                task_data.set_task_name(self.task.get_task_name())
                task_data.set_run_name(self.task.get_run_name())
                task_data.set_run_nr(self.task.get_run_nr())
                task_data.set_full_run_nr(self.task.get_full_run_nr())
                task_data.set_job_path(self.task.get_job_path())
                task_data.set_output_path(self.task.get_output_path())

                if self.task.plugin_handler.execute_hook("pre_task_function_call", {"task":self.task}):
                    print("Failing task")
                    self.task.set_task_result(rc.FAIL)
                else:
                    if len(arg_dict) > 0:
                        return_vars = target_function(task_data, **arg_dict)
                    elif len(arg_list) > 0:
                        return_vars = target_function(task_data, arg_list)
                    elif arg_single is not None:
                        return_vars = target_function(task_data, arg_single)
                    else:
                        return_vars = target_function(task_data)

                    #split return code and return variables
                    if type(return_vars) is tuple:
                        return_vars_list = list(return_vars)
                        return_code = return_vars_list[0]

                        if len(return_vars_list) > 2:
                            return_vars = tuple(return_vars_list[1:])
                        else:
                            return_vars = return_vars_list[1]
                        self.task.set_task_return_vars(return_vars)
                    else:
                        return_code = return_vars

                    self.task.set_task_result(return_code)

                if self.task.plugin_handler.execute_hook("post_task_function_call", {"task":self.task}):
                    self.task.set_task_result(rc.FAIL)

                self.task.get_logger().disable(self.task)

        except Exception:
            self.task.get_logger().disable(self.task)

            exception_string = traceback.format_exc()
            self.log.write(exception_string, 'error')

            self.task.set_task_result(rc.EXCEPTION)

        self.log.write(self.task.get_full_run_nr() + " return code: " + str(self.task.get_task_result()), 'debug')
        
        queue.put({self.task.get_run_name():self.task})


    def import_task_module(self):
        module = None
        module_name = None

        module_name = self.task.get_target_module_name()
        module_path = self.task.get_target_module_path()

        if module_path is not None and module_name is not None:
            module_path = os.path.dirname(os.path.realpath(module_path)) + '/../'
            sys.path.append(module_path)

            try:
                module = import_module(module_name)
            except Exception:
                self.log.write(traceback.format_exc(-1), 'error')
                exit(1)


        return module

    ## Retreive target function from target task module
    #  @return Target function 
    def get_function_to_run(self, module):
        function = None

        try:
            function = getattr(module, self.task.get_target_function())
        except:
            self.task.get_logger().disable(self.task)
            self.log.write("function '" + str(self.task.get_target_function()) + "' in task '" + str(self.task.get_run_name()) + "' not found", 'error')
            exit(1)

        return function
            

            
            
            

