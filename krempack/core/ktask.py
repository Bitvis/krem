
## \file task.py
## \brief Implementation of the Task class and TaskAction interface

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

import abc
import os
import sys
import pickle

from krempack.core import kconfig

class TaskData():
    
    def __init__(self):
        self.task_name = None
        self.run_name = None
        self.run_nr = None
        self.full_run_nr = None
        self.job_output_path = None
        self.output_path = None
    
    def set_task_name(self, task_name):
        self.task_name = task_name

    def set_run_name(self, run_name):
        self.run_name = run_name

    def set_run_nr(self, run_nr):
        self.run_nr = run_nr
    
    def set_full_run_nr(self, full_run_nr):
        self.full_run_nr = full_run_nr

    def set_job_path(self, root_output_path):
        self.job_output_path = root_output_path
        
    def set_output_path(self, path):
        self.output_path = path
        
    def get_task_name(self):
        return self.task_name

    def get_run_name(self):
        return self.run_name

    def get_run_nr(self):
        return self.run_nr

    def get_full_run_nr(self):
        return self.full_run_nr

    def get_job_path(self):
        return self.job_output_path
    
    def get_output_path(self):
        return self.output_path
        
class Task(TaskData):

    def __init__(self, task, run_nr):
        self.target = task
        self.target_module_name = None
        self.target_module_path = None
        self.target_function = None
        self.run_nr = run_nr
        self.action = None
        self.arguments = ""
        self.task_result = None
        self.task_return_vars = None
        self.initializer = None
        self.plugin_handler = None
        self.job_output_path = None
        self.output_path = None
        self.logger = None
        self.plugin_data = {}
        
        self.config = kconfig.Config()

    def initialize(self):
        self.initializer.execute(self)        
        
    def set_target(self, task):
        self.target = task
        
    def set_target_module_name(self, name):
        self.target_module_name = name
        
    def set_target_module_path(self, path):
        self.target_module_path = path
               
    def set_target_function(self, function):
        self.target_function = function
        
    def set_action(self, action):
        self.action = action
        
    def set_arguments(self, arguments=[]):
        self.arguments = arguments
        
    def set_initializer(self, initializer):
        self.initializer = initializer
        
    def set_task_result(self, task_result):
        self.task_result = task_result

    def set_task_return_vars(self, task_return_vars):
        self.task_return_vars = task_return_vars

    def set_plugin_handler(self, plugin_handler):
        self.plugin_handler = plugin_handler
        
    def set_logger(self, logger):
        self.logger = logger

    def set_plugin_data(self, plugin_name, data):
        self.plugin_data[plugin_name] = data

    def get_target(self):
        return self.target
    
    def get_target_module_name(self):
        return self.target_module_name
    
    def get_target_module_path(self):
        return self.target_module_path
    
    def get_target_function(self):
        return self.target_function
    
    def get_action(self):
        return self.action        
        
    def get_arguments(self):
        return self.arguments

    def get_initializer(self):
        return self.initializer        
    
    def get_task_result(self):
        return self.task_result

    def get_task_return_vars(self):
        return self.task_return_vars

    def get_plugin_handler(self):
        return self.plugin_handler
    
    def get_logger(self):
        return self.logger

    def get_plugin_data(self, plugin_name):
        return self.plugin_data[plugin_name]
###############################################
#   Class containing how the task should be 
#       executed and verified
###############################################
    
class TaskAction():
    __metaclass__ = abc.ABCMeta
    
    log = None
    name = None     # Name should be set in the implementation of the TaskAction
    
    
    def __init__(self, task):
        self.task = task #When overriding __init__: attribute 'task' must be set
        
    @abc.abstractmethod
    def run_method(self, task):
        None
    
    #   Set logger to use
    def set_logger(self, logger):
        self.log = logger    
        
    def get_name(self):
        return self.name
        
#######################################
#   Abstract Runner class
#       Inherit from this to create
#       new runner
#######################################
class TaskRun(TaskAction):
    __metaclass__ = abc.ABCMeta
    name = 'run'
    
