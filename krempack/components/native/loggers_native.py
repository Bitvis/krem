#!/usr/bin/env python
## \file loggers_native.py
## \brief Default implementation of logger classes

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

import sys
import os
import re

from krempack.components import loggers

RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0;0m"

## Native job logger
#
# Log and print job activity
class JobLoggerNative(loggers.JobLogger):   
    
    ## Constructor
    def __init__(self):
        self.log_levels = ['debug', 'info', 'warn', 'error'] 
        log_level_color = [CYAN, RESET, YELLOW, RED]
        
        self.log_level_color = {} 
        counter = 0
        for log_level in self.log_levels:
            self.log_level_color[log_level] = log_level_color[counter]
            counter = counter + 1
        
        self.log_level = 'info'
    
    ## Log/print job activity
    def write(self, text, level):
        if self.check_log_level(level):             # Skip if log level is lower than current setting
            log_text = self.format_entry(text, level)
            self.set_text_color(level)
            print(log_text)
            self.reset_text_color()
            self.write_to_log(log_text + '\n')
        return

    ## Applies formatting of log entry
    def format_entry(self, text, level):
        return "[" + level.upper() + "]: " + text
    
    ## Checks if level of log entry is ><= than current settings 
    def check_log_level(self, level):
        level_ok = False
        nLevel = 0
        nLog_level = 0
        for c, l in enumerate(self.log_levels, 1):
            if level is l:
                nLevel = c
            if self.log_level is l:
                nLog_level = c
        if nLevel is not 0 and nLog_level is not 0:
            if nLevel >= nLog_level:
                level_ok = True
        else:
            print("[INTERNAL_ERROR]: Provided log level not found")
            exit(1)
        return level_ok
   
    ## Set log level
    def set_log_level(self, level):
        if level in self.log_levels:
            self.log_level = level
        else:
            print("[INTERNAL_ERROR]: Assigned log level does not exist")
            exit(1)

    ## Apply text color based on log level
    def set_text_color(self, log_level):
        sys.stdout.write(self.log_level_color[log_level])

    ## Reset text color
    def reset_text_color(self):
        sys.stdout.write(RESET)

## Native results logger
class ResultsLoggerNative(loggers.ResultsLogger):
    
    ## Constructor
    def __init__(self):
        self.results = []
        self.result_text = []
    
    ## Write to results log
    def write(self, task_list=[]):
        codes_list = self.code_parser.get_codes_list() 
        for code in codes_list:
            self.results.append((code,0))
        
        self.result_text.append('{0:40} {1}'.format('TASK', 'RESULT') + '\n\n')
        
        # Summarize results
        for task in task_list:
            if task.get_task_result() is not None:
                parsed_result = self.code_parser.parse(task.get_task_result())
                self.result_text.append('{0:40} {1}'.format(task.get_task_name(), parsed_result) + '\n')
                for i, entry in enumerate(self.results):
                    if parsed_result is entry[0]:
                        self.results[i] = (entry[0], int(entry[1]) + 1)
            else:
                self.job_logger.write('No results found for task: ' + task.get_task_name(), 'warn')
  
            
        self.result_text.append('\nSUMMARY:\n\n')
            
        # Create log text (with formatting)
        for entry in self.results:
            self.result_text.append('{0:20} {1}'.format(str(entry[0]),str(entry[1])) + '\n')
        
        self.write_to_log(self.result_text)
        
## Writer class
#
# Used by TaskLoggerNative for overriding print-function to write to task log
class TaskWriter:
    ## Constructor
    def __init__(self, tag, output_file):
        self.output_file = output_file
        self.tag = tag
    
    ## Replaces print-function in tasks
    def write(self, text):
        logfile = open(self.output_file, "a", os.O_NONBLOCK)
        for line in text.splitlines():
            if line and line.strip():
                logfile.write(self.tag)
                logfile.write(line)
                logfile.write("\n")
        logfile.close()

## Native task logger
#   
# Logs task output to global log file by redirecting stdout to log file.
class TaskLoggerNative(loggers.TaskLogger):
    
    logFileName = "tasks.log"
    stdout_default = sys.stdout
    stderr_default = sys.stderr
    
    def __init__(self):
        self.log_file_path = None
        self.task_tag = None
    
    ## Activate logger by redirecting stdout to TaskWriter
    def enable(self, task):
        prefix = re.search("^\d+", task.get_task_name())
        postfix = re.search("\d+$", task.get_task_name())
        if prefix and postfix:
            self.task_tag = str(prefix.group(0)) + "_" + str(postfix.group(0)) + ": "

        logfile = open(self.log_file_path, "a", os.O_NONBLOCK)
        sys.stdout = logfile
        sys.stderr = logfile
        print("\n" + self.task_tag + "*** Task start: " + str(task.task_name) + " ***\n")
        logfile.close()
        
        task_writer = TaskWriter(self.task_tag, self.log_file_path)
        sys.stdout = task_writer
        sys.stderr = task_writer
        
    ## Disables logger and restores default stdout
    def disable(self, task):
        logfile = open(self.log_file_path, "a", os.O_NONBLOCK)
        sys.stdout = logfile
        sys.stderr = logfile
        print("\n" + self.task_tag + "*** Task end: " + str(task.task_name) + " ***\n")
        logfile.close()
        
        sys.stdout = self.stdout_default
        sys.stderr = self.stderr_default
        
    def set_log_file(self, path):
        self.log_file_path = os.path.abspath(path)

    

