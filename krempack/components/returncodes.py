
## \file returncodes.py
## \brief Interface classes to the return code parser

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

########################################
# Return codes class
########################################
class ReturnCodes():
    pass
    


########################################
#   For parsing return code from external
#       executables (for instance a task script
########################################
class ReturnCodeParser():
    
    @abc.abstractmethod
    def parse(self, return_code):
        None
        
    @abc.abstractmethod
    def get_codes_list(self):
        None
