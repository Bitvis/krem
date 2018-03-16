
## \file returncodes_native.py
## \brief Default implementation of return code classes

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

import os
import sys
import abc

from krempack.components import returncodes


class ReturnCodeParserNative(returncodes.ReturnCodeParser):
    
    # function 'get_codes_list' generates list of attributes in class 'ReturnCodesNative' dynamically by
    # searching all variables of the class. This is done by retrieving 'items()' from the class,
    # which also retreives some unwanted values. These are listed in ATTR_IGNORE
    ATTR_IGNORE = ['__doc__', '__main__', '__module__', '__weakref__', '__dict__']
    returncodes = None
    
    def __init__(self, returncodes):
        self.returncodes = returncodes
        
    def parse(self, return_code):
        return_string = None
        
        for attr, code_value in vars(self.returncodes).items():
            if attr not in self.ATTR_IGNORE:
                if return_code is code_value:
                    return_string = attr
        
        if return_string is None:
            return_string = 'UNKNOWN'
            
        return return_string
    
 
    def get_codes_list(self):
        codes_list = []
        for attr, code_value in vars(self.returncodes).items():
            if attr not in self.ATTR_IGNORE:
                codes_list.append(attr)

        codes_list.sort()
        return codes_list
            
    def set_returncodes(self, returncodes):
        self.returncodes = returncodes
      
