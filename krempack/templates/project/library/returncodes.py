## \file returncodes.py
## \brief Implementation of return codes

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


class ReturnCodes():
    # the following codes might be used internally by KREM and MUST NOT be removed
    EXCEPTION = 6

    # Add or remove your return codes here
    PASS = 0
    FAIL = 1
    SUCCESS = 2
    ERROR = 3
    SKIPPED = 4
    UNSTABLE = 5


# TRUE = 6
# FALSE = 7

# make an alias to ReturnCodes so jobs and tasks have 1 line less to add :-)
rc = ReturnCodes
