
## \file kremtree.py
## \brief Functions for assisting project tree navigation

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
from krempack.common import constants as c

###############################################
#    Returns list of directories within target 
#        path
###############################################
def list_dir(target_path):
    dirlist = []
    for d in os.listdir(target_path):        
        path = os.path.join(target_path, d)
        if os.path.isdir(path):
            dirlist.append(d)
    return dirlist

###############################################
#    Returns relative path to target common 
#        directory within the project
#        directory (eg. 'library', 'jobs', 'tasks'). 
###############################################
def find_common_dir(target):
    kremRoot = find_krem_root('./')

    if kremRoot is not None and os.path.isdir(os.path.join(kremRoot, target)):
        relPath = os.path.join(kremRoot, target)
    else:
        print('ERROR: Project root directory not found.')
        relPath = None
        exit(1)

    return relPath

###############################################
#    Returns relative path to root of 
#        project dir. Returns None
#        if pwd is not located inside 
#        project dir	 
###############################################
def find_krem_root(startPath):
    if not is_root_path(startPath):
        entries = os.listdir(startPath)
 
        found = True
        for target in c.PROJECT_DEFAULT_DIRS:
            if target not in entries:                
                found = False
        if found is True:
            returnValue = os.path.relpath(startPath)
        else:
            returnValue = find_krem_root(os.path.join(startPath, '..'))
    else:
        returnValue = None

    return returnValue


################################################
#    Check if given path is at system root
#        (function required for cross platform)
################################################   
def is_root_path(path):
    return os.path.abspath(path) == os.path.abspath(os.sep)


