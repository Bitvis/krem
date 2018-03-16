
## \file colors.py
## \brief Implementation of color codes

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


class ColorCodes():
    # the following codes are used internally by KREM and MUST NOT be removed
    RED = "\033[1;31m"
    YELLOW = "\033[1;33m"
    CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"
    GRAY = "\033[1;30m"

    RESET = "\033[0;0m"
    ERROR = RED
    WARN = YELLOW
    DEBUG = CYAN

    # Add or remove color codes here



#make an alias to ReturnCodes so jobs and tasks have 1 line less to add :-)
cc = ColorCodes
