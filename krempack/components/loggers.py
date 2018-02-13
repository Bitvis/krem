
## \file loggers.py
## \brief Interfaces to logger classes

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

import abc
import os
import re

## Virtual logger class
#
# Parent to all loggers
class Logger:
    __metaclass__ = abc.ABCMeta
    
    logFileName = ""
    
    ## Constructor
    def __init(self):
        self.log_file_path = None
    
    ## Set and create empty log file
    def set_log_file(self, path):
        self.log_file_path = os.path.abspath(path)
        f = open(path, 'w')
        f.close()
    
    ## Set name of log file
    def set_log_file_name(self, name):
        self.logFileName = name
    
    ## Get name of log file
    def get_log_file_name(self):
        return self.logFileName
        
    ## Get path to log file
    def get_log_file(self):
        return self.log_file_path
    
    ## Write to log file
    def write_to_log(self, text):
        try:
            f = open(self.log_file_path, 'a')
            if hasattr(text, "__iter__"):
                for line in text:
                    f.write(str(line))
            else:
                f.write(str(text))
            f.close()
        except Exception as e:
            print("[INTERNAL_EXCEPTION]: " + str(e))

    ## Strip of color codes from text
    def strip_coloring(self, text):
        regexp = r"" + re.escape("\033[") + r"[0|1];.{1,2}m"
        return re.sub(regexp, '', text)
        
    
## Virtual job logger
#
# Logs all job activity
class JobLogger(Logger):
    __metaclass__ = abc.ABCMeta
    
    logFileName = "execution.log"
    ## Constructor
    @abc.abstractmethod
    def __init__(self):
        None
   
    ## Write to log
    @abc.abstractmethod
    def write(self, text, level):
        None
        

## Virtual results logger
#
#   For logging collective results after tasks have been run.
#       Intentional use is to take the return code from each
#       task (stored within Task-object) in order to produce
#       the results. Parsing return codes into 'pass', 'fail',
#       etc. is performed by ReturnCodeParser
class ResultsLogger(Logger):
    
    logFileName = "results"
    
    ## Constructor
    def __init__(self):
        self.code_parser = None
        self.job_logger = None
    
    ## Write to log
    @abc.abstractmethod
    def format_results(self, task_list=[]):
        None
    
    ## Set job logger for logging internal activity
    def set_job_logger(self, logger):
        self.job_logger = logger
        
    ## Set ReturnCodeParser for getting results
    def set_code_parser(self, parser):
        self.code_parser = parser
        
## Virtual task logger
#
#   Logs task output to global log file.
class TaskLogger(Logger):
    
    logFileName = "tasks.log"
    
    ## Constructor
    @abc.abstractmethod
    def __init__(self):
        None

    ## Enable logging
    @abc.abstractmethod
    def enable(self, task):
        None
    
    ## Disable logging
    @abc.abstractmethod
    def disable(self, task):
        None        
        
    ## Set job logger for logging internal activity
    def set_job_logger(self, logger):
        self.job_logger = logger
        

    
