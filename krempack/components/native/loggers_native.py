
## \file loggers_native.py
## \brief Default implementation of logger classes

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

import sys
import os
import re

from krempack.components import loggers
mod = __import__('library.colorcodes', fromlist=['ColorCodes'])
cc = getattr(mod, 'cc')


## Native job logger
#
# Log and print job activity
class JobLoggerNative(loggers.JobLogger):   
    
    ## Constructor
    def __init__(self):
        self.log_levels = ['debug', 'info', 'warn', 'error'] 
        log_level_color = [cc.DEBUG, cc.RESET, cc.WARN, cc.ERROR]
        
        self.log_level_color = {} 
        counter = 0
        for log_level in self.log_levels:
            if log_level != 'none':
                self.log_level_color[log_level] = log_level_color[counter]
                counter = counter + 1
        
        self.log_level = 'info'
    
    ## Log/print job activity
    def write(self, text, level=None):
        if self.check_log_level(level):             # Skip if log level is lower than current setting
            log_text = self.format_entry(text, level)

            #If in task context, print to task log and redirect stdout to terminal
            stdout_saveout = None
            if sys.stdout != sys.__stdout__:
                print(log_text)
                stdout_saveout = sys.stdout
                sys.stdout = sys.__stdout__

            self.set_text_color(level)
            print(log_text)
            self.reset_text_color()

            #reset stdout
            if stdout_saveout is not None:
                sys.stdout = stdout_saveout

            log_text = self.strip_coloring(log_text)
            self.write_to_log(log_text)
        return


    ## Applies formatting of log entry
    def format_entry(self, text, level):
        format_string = text
        if level is not None:
            format_string = "[" + level.upper() + "]: " + format_string
        return format_string
    
    ## Checks if level of log entry is ><= than current settings 
    def check_log_level(self, level):
        level_ok = False

        if level is None:
            level_ok = True
        else:
            nLevel = 0
            nLog_level = 0
            for c, l in enumerate(self.log_levels, 1):
                if level == l:
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
        if log_level is not None:
            sys.stdout.write(self.log_level_color[log_level])

    ## Reset text color
    def reset_text_color(self):
        sys.stdout.write(cc.RESET)

## Native results logger
class ResultsLoggerNative(loggers.ResultsLogger):
    
    ## Constructor
    def __init__(self):
        self.results = []

    
    ## Write to results log
    def format_results(self, task_list=[]):
        results = ""

        codes_list = self.code_parser.get_codes_list() 
        for code in codes_list:
            self.results.append((code,0))


        #find the longest task_name to set offset for the function column
        func_offset = 0
        for task in task_list:
            if func_offset < len(task.get_task_name()):
                func_offset = len(task.get_task_name())

        # add some more to compensate for the full run nr length
        func_offset += 10

        result_offset = 0
        for task in task_list:
            if result_offset < len(task.get_target_function()):
                result_offset = len(task.get_target_function())
        result_offset += 5

        results += ('{0:{func_offset}} {1:{result_offset}} {2}'.format('        TASK', 'FUNCTION', 'RESULT', func_offset=func_offset, result_offset=result_offset) + '\n\n')
        
        # Summarize results
        for task in task_list:
            if task.get_task_result() is not None:
                parsed_result = self.code_parser.parse(task.get_task_result())

                results += '{0:8}{1}{2:{func_offset}} {3}{4:{result_offset}} {5}{6}'.format(task.get_full_run_nr(), cc.WHITE, task.get_task_name(),
                                                                                                      cc.YELLOW, task.get_target_function(), cc.RESET, parsed_result,
                                                                                                      func_offset=func_offset-8, result_offset=result_offset) + '\n'
                for i, entry in enumerate(self.results):
                    if parsed_result is entry[0]:
                        self.results[i] = (entry[0], int(entry[1]) + 1)
            else:
                self.job_logger.write('No results found for task: ' + task.get_run_name(), 'warn')
  
            
        results += '\nSUMMARY:\n\n'
            
        # Create log text (with formatting)
        for entry in self.results:
            results += '{0:20} {1}'.format(str(entry[0]),str(entry[1])) + '\n'

        #make two variants, one with colors and one without
        results_colored = results

        results = self.strip_coloring(results)

        return results, results_colored
        
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
        #for real files O_NONBLOCK has no effect so we change from O_NONBLOCK to O_WRONLY
        logfile = open(self.output_file, "a", os.O_WRONLY)
        for line in text.splitlines():
            if line and line.strip():
                logfile.write(self.tag + "  ")
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

    ## Activate logger by redirecting stdout to TaskWriter
    def enable(self, task):

        logfile = open(self.log_file_path, "a", os.O_WRONLY)
        sys.stdout = logfile
        sys.stderr = logfile
        print("\n" + task.get_full_run_nr() + "  *** Task start: " + "  " + task.get_task_name() + "  " + task.get_target_function() + " ***\n")
        logfile.close()
        
        task_writer = TaskWriter(task.get_full_run_nr(), self.log_file_path)
        sys.stdout = task_writer
        sys.stderr = task_writer
        
    ## Disables logger and restores default stdout
    def disable(self, task):
        logfile = open(self.log_file_path, "a", os.O_WRONLY)
        sys.stdout = logfile
        sys.stderr = logfile
        print("\n" + task.get_full_run_nr() + "  *** Task end: " + str(task.task_name) + " ***\n")
        logfile.close()
        
        sys.stdout = self.stdout_default
        sys.stderr = self.stderr_default
        
    def set_log_file(self, path):
        self.log_file_path = os.path.abspath(path)



