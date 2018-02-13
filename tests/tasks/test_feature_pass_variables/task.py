#!/bin/env python
import sys
import os
from library.returncodes import *
from library.testlib import parameters as p


def run_variable_list(task, test_var_list):

    result = rc.UNSTABLE
    print("Expected variable list: " + str(p.test_var_list))
    print("variables passed from job to task: " + str(test_var_list))
    
    if test_var_list is None:
        print("ERROR: No variables passed from job to task")
        result = rc.FAIL
    elif test_var_list != p.test_var_list:
        print("ERROR: Variable list passed from job to task is not as expected")
        result = rc.FAIL
    else:
        print("Variable list passed from job to task OK")
        result = rc.PASS
        
    return result
        
def run_named_variables(task, test_var_1, test_var_2):

    result = rc.PASS
    
    print("Expected variables:")
    print("test_var_1: "+ str(p.test_var_1))
    print("test_var_2: "+ str(p.test_var_2))
    print("variables passed from job to task:")
    print("test_var_1: "+ str(test_var_1))
    print("test_var_2: "+ str(test_var_2))

    if test_var_1 is None:
        print("ERROR: test_var_1 is empty")
        result = rc.FAIL
    elif test_var_1 != p.test_var_1:
        print("ERROR: test_var_1 does not match expected")
        result = rc.FAIL
    
    if test_var_2 is None:
        print("ERROR: test_var_2 is empty")
        result = rc.FAIL
    elif test_var_2 != p.test_var_2:
        print("ERROR: test_var_2 does not match expected")
        result = rc.FAIL
    
    if not result:
        print("Variables passed from job to task OK")
        result = rc.PASS
        
    return result
