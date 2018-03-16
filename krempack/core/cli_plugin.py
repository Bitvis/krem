
## \file cli_plugin.py
## \brief Function for setting up cli plugins

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

import sys
import os

from importlib import import_module

from krempack.common import kremtree
from krempack.common import constants as c

def setup_cli_plugins(plugin_handler):
    success = True
    module_name = "library.setup"
    module_path = os.path.abspath(kremtree.find_krem_root('.'))
    sys.path.append(module_path)

    try:
        module = import_module(module_name)
    except Exception as e:
        #print("[ERROR]: Failed to import 'setup.py' in " + str(module_path))
        #print("Exception raised: " + str(e))
        #exit(1)
        # Never cause error until v3.0.0, to maintain backwards compatibility
        success = False

    try:
        module.setup_cli_plugins(plugin_handler)
    except Exception as e:
        #print("[ERROR]: Failed to run 'setup_cli_plugins' in " + os.path.join(module_path, "library", "setup.py"))
        #print("Exception raised: " + str(e))
        #exit(1)
        # Never cause error until v3.0.0, to maintain backwards compatibility
        success = False

    if success:
        for hook in plugin_handler.hook_names:
            plugin_handler.hooks[hook].synch_call_lists()

    return success