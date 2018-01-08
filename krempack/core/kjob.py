#!/usr/bin/env python
## \file core.py
## \brief Implementation of the Job class

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
import inspect
import sys

from krempack.core import ktask
from krempack.core import kconfig
from krempack.core import executor
from krempack.core import taskaction
from krempack.core import plugin

from krempack.components.native import returncodes_native
from krempack.components.native import initializers_native
from krempack.components.native import validator_native
from krempack.components.native import loggers_native

from krempack.common import constants as c
from krempack.common import kremtree

class Job():
    executor = executor.Executor()
    validator = validator_native.Validator()
    taskaction = taskaction.TaskAction
    plugin_handler = plugin.PluginHandler()

    # Job initiated with all default components
    def __init__(self, name, returncodes, func=None):  
        self.task_list = []
        self.task_run_nr = 1
        self.task_list_index = -1
        self.name = name
        
        self.config = kconfig.JobConfig() 
        
        self.config.set_job_initializer(initializers_native.JobInitializerNative())
        
        self.config.set_task_initializer_default(initializers_native.TaskInitializerNative) #Do not create instance here, as each task requires it's own instance
        
        self.config.set_return_code_parser(returncodes_native.ReturnCodeParserNative(returncodes))
        
        self.config.set_environ(os.environ.copy())
        
        self.config.set_job_logger(loggers_native.JobLoggerNative())
        
        self.config.set_result_logger(loggers_native.ResultsLoggerNative())
        
        self.config.set_task_logger(loggers_native.TaskLoggerNative) #Do not create instance here, as each task requires it's own instance

        
    def start(self): 
        for entrypoint in c.plugin_entry_points:
            self.plugin_handler.entrypoints[entrypoint].synch_call_lists()
        
        self.plugin_handler.entrypoints["job_configuration"].execute({"job":self})
        
        initializer = self.config.get_job_initializer()
        root_output_path = initializer.execute(self.name)
        
        if self.config.get_root_output_path() is None:
            self.config.set_root_output_path(root_output_path)
            
        
        log_path = os.path.join(self.config.get_root_output_path(), self.config.get_job_logger().get_log_file_name())
        self.config.get_job_logger().set_log_file(log_path)
        
        
        log_path = os.path.join(self.config.get_root_output_path(), self.config.get_result_logger().get_log_file_name())
        self.config.get_result_logger().set_log_file(log_path)
            
            
        self.validator.set_logger(self.config.get_job_logger())
        self.executor.set_logger(self.config.get_job_logger())
        
        self.log = self.config.get_job_logger()
       
    # Load configuration object
    # Must not just set the new config object, as user has most likely not 
    # set all attributes. Merging the default and new config allows for 
    # default settings to remain if user has not set a target attribute
    def load_config(self, conf):
        
        if isinstance(conf, kconfig.JobConfig):
            if conf.job_logger is not None:
                self.config.set_job_logger(conf.job_logger)
            if conf.task_log_path is not None:
                self.config.set_task_logger(conf.task_logger)
            if conf.root_output_path is not None:
                self.config.set_root_output_path(conf.root_output_path)
            if conf.job_initializer is not None:
                self.config.set_job_initializer(conf.job_initializer)
            if conf.result_logger is not None:
                self.config.set_result_logger(conf.result_logger)
            if conf.return_code_parser is not None:
                self.config.set_return_code_parser(conf.return_code_parser)
            if conf.task_initializer_default is not None:
                self.config.set_task_initializer_default(conf.task_initializer_default)
            if conf.task_initializer_default is not None:
                self.config.set_environ(conf.get_environ)       
                
                
            self.log.write("Loaded new configurations", "info")
        else:
            self.log.write("Provided Config object is not a subclass of JobConfig", "error")
            exit(1)
            
        
    # Creates new object 'Task'. The object parameters are initialized in this function,
    # however the output directory is not created until required (performed by TaskInitializer)
    def add_task(self, task, function, variables=None, task_logger=None, task_initializer=None):
        
        new_task = ktask.Task(task, self.task_run_nr)
        new_task.set_plugin_handler(self.plugin_handler)
        new_task.set_environ(self.config.get_environ())
        new_task.config.set_root_output_path(self.config.get_root_output_path())
        new_task.set_action(self.taskaction())
        new_task.get_action().set_target_task(new_task)
        
        # Set target function to call in target task
        new_task.set_target_function(function)   
        
        if variables is not None:
            new_task.set_variables(variables)
            
        if task_logger is not None:
            new_task.set_logger(task_logger())
        else:
            new_task.set_logger(self.config.get_task_logger()())
            
        log_path = os.path.join(self.config.get_root_output_path(), new_task.get_logger().get_log_file_name())
        new_task.get_logger().set_log_file(log_path)
           
            
        if task_initializer is not None:
            new_task.set_initializer(task_initializer)
        else:
            new_initializer = self.config.task_initializer_default()
            new_task.set_initializer(new_initializer)  
            
            
        new_task.initializer.set_logger(self.config.get_job_logger())
        new_task.action.set_logger(self.config.get_job_logger())
            
        self.task_list.append(new_task)
        
        new_task.initializer.compile_task_module_name_and_path(new_task)
        new_task.initializer.generate_task_name(new_task, self.task_list) # Must be called here, as task name is used before task initializer is executed
        
        
        
        self.task_list_index = self.task_list_index + 1
        
    def add_invalid_task(self, task):
        
        new_task = ktask.Task(task, self.task_run_nr)
        new_task.set_task_result(1)
        new_task.set_task_name("task: " + str(task))
            
        self.task_list.append(new_task)
        
        self.task_list_index = self.task_list_index + 1
    
    ############################
    #   Executors
    ############################
    
    # Wait until task(s) are complete. returns task result accordingly:
        #if only a single task returned code !=0, then return that code,
        #else if more than one task returned !=0, but the return code is the same for all, then return that code
        #else if more than one task returned !=0, and codes differ then return 1
    def update_on_complete(self):
        ret = 0
        self.executor.wait_until_all_complete()
        task_results = self.get_task_results(self.task_run_nr)
        
        for task in self.task_list:
            if task.get_run_nr() == self.task_run_nr:
                self.plugin_handler.entrypoints["task_post_processing"].execute({"task":task, "job":self})
        self.task_run_nr = self.task_run_nr + 1
                
        for task_result in task_results:
            if task_result != 0: 
                if ret == 0:
                    ret = task_result                
                elif ret != task_result:
                    ret = 1
                    break            
        return ret      
    
    # Run single task and wait until complete
    def run_task_serial(self, task, function, variables=None, task_logger=None, task_initializer=None):
        ret = 1
        
        ret = self.validator.validate(task)
        
        if not ret:
            self.add_task(task, function, variables=variables, task_logger=task_logger, task_initializer=task_initializer)

            if self.executor.is_ready():
                self.plugin_handler.entrypoints["pre_task_setup"].execute({"task":task, "job":self})
                self.executor.execute(self.task_list[self.task_list_index])
                ret = self.update_on_complete()
            else:
                self.log.write('Unable to execute task: ' + self.task_list[self.task_list_index].task_name, 'error')
                self.log.write('Parallel tasks executed, but not completed', 'error')
                self.log.write('Aborting job...', 'error')
                exit(1)
        else:
            self.add_invalid_task(task)
        return ret     
        
    # Run single task and continue immediately. Call multiple times to run tasks in parallel. Must call update_on_complete()
    # in job before running new run_task_serial or end of job
    def run_task_parallel(self, task, function, variables=None, task_logger=None, task_initializer=None):
        error = self.validator.validate(task)
        
        if not error:
            self.add_task(task, function, variables=variables, task_logger=task_logger, task_initializer=task_initializer)
            self.executor.execute(self.task_list[self.task_list_index])
        else:
            self.add_invalid_task(task)

    
    # Parse and log results. The results are collected from each Task in the result logger
    def compile_results(self):
        
        if self.executor.is_ready():
            result_logger = self.config.get_result_logger()

            result_logger.set_job_logger(self.config.get_job_logger())
            result_logger.set_code_parser(self.config.get_return_code_parser())

            # Write to log
            result_logger.write(self.task_list)

            # Print log to screen
            print('\n')
            print('---------------------------------------------------------')
            with open(result_logger.get_log_file(), 'r') as f:
                print(f.read())

            print('---------------------------------------------------------')
            print('\n')

            self.log.write('Results written to: ' + result_logger.get_log_file(), 'info')
        else:
            self.log.write('Parallel tasks not completed before end of job', 'error')
            self.log.write('Aborting job...', 'error')
            exit(1)
        
    #return a list with results from all tasks
    def get_task_results(self, run_nr=0):
        task_results = []
        for task in self.task_list:
            if run_nr is 0 or task.run_nr is run_nr:
                task_results.append(task.task_result)
        return task_results

    #if only a single task returned code !=0, then return that code,
    #else if more than one task returned !=0, but the return code is the same for all, then return that code
    #else if more than one task returned !=0, and codes differ then return 1
    def get_job_result(self):
        task_results = self.get_task_results()
        ret = 0
        
        for task_result in task_results:
            if task_result != 0: 
                if ret == 0:
                    ret = task_result                
                elif ret != task_result:
                    ret = 1
                    break            
        return ret        
    
    def end(self):
        self.compile_results()
        self.plugin_handler.entrypoints["job_post_processing"].execute({"job":self})
