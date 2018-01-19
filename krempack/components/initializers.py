
## \file initializers.py
## \brief Interfaces to initializer classes

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
import sys

from krempack.core import ktask

class Initializer():
    __metaclass__ = abc.ABCMeta

    
    def __init__(self):
        self.log = None
        
    #   Set logger to use
    def set_logger(self, logger):
        self.log = logger

    @abc.abstractmethod
    def execute(self, target):
        None
        
class JobInitializer(Initializer):
    __metaclass__ = abc.ABCMeta
    
    
class TaskInitializer(Initializer):
    __metaclass__ = abc.ABCMeta

    # Used for generating a name for the task, which is also used for the output directory
    @abc.abstractmethod
    def generate_task_name(self, new_task, task_list=[]):
        None
