
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
        self.tasksRunning[task.get_run_name()] = task
        p.start()        

    def wait_until_all_complete(self):
        '''
        The queue implementation in multiprocessing that allows data to be transferred between processes relies on standard OS pipes.
        OS pipes are not infinitely long, so the process which queues data could be blocked in the OS during the put() operation until some other process uses get() to retrieve data from the queue.
        For small amounts of data, the main process can join() all the spawned subprocesses and then pick up the data. This often works well, but does not scale, and it is not clear when it will break.
        But it will certainly break with large amounts of data. The subprocess will be blocked in put() waiting for the main process to remove some data from the queue with get(), but the main process is blocked in join() waiting for the subprocess to finish. This results in a deadlock.
        '''

        still_running = len(self.procsRunning)

        #we empty the queue before we join all subprocesses to avoid deadlock
        while still_running > 0:
            if not self.queue.empty():
                entry = self.queue.get()
                run_name, task = entry.popitem()

                try:
                    self.tasksRunning[run_name].set_task_result(task.get_task_result())
                except Exception as e:
                    self.log.write("Failed to retrieve task results", 'error')
                still_running = still_running - 1

            for proc in self.procsRunning:
                if not proc.is_alive() and proc.exitcode != 0:
                    #process exited abnormally, probably crashed or syntax error
                    #kill all processes still running
                    for proc in self.procsRunning:
                        if proc.is_alive():
                            proc.terminate()
                    exit(1)

        #all processes have now exited
        for proc in self.procsRunning:
            if not proc.is_alive():
                #call join() with timeout and catch exception if we hang here again
                proc.join()

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

    
  

    
    
        

