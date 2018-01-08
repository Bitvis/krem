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

'''
description: 
    Provides access from a task script of the corresponding task object living inside KREM
'''
import sys
import os

from krempack.common import constants as c

from krempack.core import ktask
from library.returncodes import ReturnCodes

#make an alias to ReturnCodes so the tasks has 1 line less to add :-)
rc = ReturnCodes
