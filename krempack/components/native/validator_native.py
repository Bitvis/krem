
## \file validator_native.py
## \brief Default implementation of validator classes

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

from krempack.components import validator
from krempack.common import kremtree
from krempack.common import constants as c
import os

# Executes method 'verify()' in all tasks TaskAction
class Validator(validator.Validator):
   
    def validate(self, task):
        error = 0
        task_path = os.path.realpath(os.path.join(kremtree.find_krem_root('./'), c.PROJECT_TASKS_DIR, task))
        
        # Check task folder
        if not os.path.isdir(task_path):
            self.log.write("Task folder " + str(task_path) + " not found", 'error')
            error = 1
        
        # Check setup file
        if not error and not os.path.isfile(os.path.join(task_path, c.TEMPLATE_TASK_SETUP_FILE)):
            self.log.write("Setup file not found in " + str(task_path), 'error')
            error = 1
            
        if not error and not os.path.isfile(os.path.join(task_path, c.TEMPLATE_INIT_PACKAGE_FILE)):
            self.log.write("task folder " + str(task_path) + " is not a python package. Please add file '__init__.py'" , 'error')
            error = 1
            
        return error
