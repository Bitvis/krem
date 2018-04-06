#!/bin/env python

import os
import shutil

from library.returncodes import *
from library.testlib import parameters as p

def run(task):
    
    result = rc.PASS
    # Init test project    
    
    if os.path.isdir(p.TEMP_PROJECT_PATH):
        try:
            shutil.rmtree(p.TEMP_PROJECT_PATH)
        except Exception:
            print("ERROR: Failed to remove " + str(p.TEMP_PROJECT_PATH))
            result = rc.FAIL
    else:
        print("WARNING: " + p.TEMP_PROJECT_PATH + " does not exist.")
        rc.SKIPPED
        
    if result == rc.PASS:
        print("Removed directory: " + str(p.TEMP_PROJECT_PATH))
    return result