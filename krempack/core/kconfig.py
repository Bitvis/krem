
## \file kconfig.py
## \brief Declaration and implementation of configuration classes

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

class Config():
    
    def __init__(self):
        self.job_logger = None
        self.root_output_path = None
        self.task_logger = None
    
    
    def set_job_logger(self, logger):
        self.job_logger = logger
    
    def set_task_logger(self, logger):
        self.task_logger = logger
        
    def set_root_output_path(self, path):
        self.root_output_path = path
        
    def get_job_logger(self):
        return self.job_logger
    
    def get_task_logger(self):
        return self.task_logger
    
    def get_root_output_path(self):
        return self.root_output_path

    
    
    
    
class JobConfig(Config):
    
    def __init__(self):
        self.job_logger = None
        self.task_log_path = None
        self.root_output_path = None
        self.job_initializer = None
        self.result_logger = None
        self.return_code_parser = None
        self.task_initializer_default = None
        self.task_logger = None
    
    def set_job_initializer(self, initializer):
        self.job_initializer = initializer
        
    def set_result_logger(self, logger):
        self.result_logger = logger
        
    def set_return_code_parser(self, return_code_parser):
        self.return_code_parser = return_code_parser
    
    def set_task_initializer_default(self, initializer):
        self.task_initializer_default = initializer
        
    def get_task_initializer_default(self):
        return self.task_initializer_default
    
    def get_job_initializer(self):
        return self.job_initializer
    
    def get_result_logger(self):
        return self.result_logger
    
    def get_return_code_parser(self):
        return self.return_code_parser
        

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                        

