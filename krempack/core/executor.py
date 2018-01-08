#!/usr/bin/env python
## \file executor.py
## \brief Job execution class

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
import sys
from multiprocessing import Process, Queue

from krempack.core import ktask


#################################################
#    Executor class
#       execute_...() provide execution order
#       functionality. They execute abstract function
#       'run_method()' with dedicated order on list of Task 
#       objects. Implement function execute() by 
#       pointing to required execution order function, 
#       and implement what to execute in function 'run_method()'
#################################################
class Executor(): 
    
    log = None
    procsRunning = []
    tasksRunning = {}
    queue = Queue()
    
    #   Set logger to use
    def set_logger(self, logger):
        self.log = logger
    
    #   Executes run_method() on each TaskAction within all Tasks in semi parallel order. 
    #   All Tasks with same run_nr are parallel
    def execute(self, task, override=None):
        p = Process(target=task.action.run_method, args=(self.queue,))
        self.procsRunning.append(p)
        self.tasksRunning[task.get_task_name()] = task
        p.start()        

    def wait_until_all_complete(self):
        for proc in self.procsRunning:
            proc.join()
            
        while not self.queue.empty():
            entry = self.queue.get()
            task_name, task = entry.popitem()
        
            try:
                self.tasksRunning[task_name].set_task_result(task.get_task_result())
            except Exception as e:
                self.log.write("Failed to retreive task results", 'error')
        
        self.tasksRunning = {}
        self.procsRunning = []
            
    def is_ready(self):
        ret = False
        
        if len(self.procsRunning) is 0:
            ret = True
            
        return ret
            
    def sort_task_list(self, task_list=[]):
        return sorted(task_list, key=lambda ktask: ktask.run_nr)
    
    def check_list(self, task_list=[]):
        if task_list is None:
            self.log.write("No tasks found", 'error')
            exit(1)

    
  

    
    
        

