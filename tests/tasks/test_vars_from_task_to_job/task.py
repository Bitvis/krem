#!/bin/env python
from library.returncodes import *

import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".."))
from library.testlib import parameters as p

from krempack.core.ktask import TaskData


def return_single_variable(task):
    return rc.PASS, p.test_arg_1

def return_list_variable(task):
    return rc.PASS, p.test_arg_list

def return_three_variables(task):
    return rc.PASS, p.test_arg_1, p.test_arg_list, p.test_arg_dict

def return_object(task):
    return rc.PASS, task



def check_vars(task, test, var_ret, var):

    ret = rc.FAIL

    print('test: ' + test)
    print('var_ret: ' + str(var_ret))
    print('var: ' + str(var))

    if test == 'return_single_variable':
        if var == p.test_arg_1:
            ret = rc.PASS

    elif test == 'return_list_variable':
        if var == p.test_arg_list:
            ret = rc.PASS

    elif test == 'return_three_variables':
        p_list = [p.test_arg_1, p.test_arg_list, p.test_arg_dict]
        p_tuple = tuple(p_list)
        print(str(p_tuple))
        if var == p_tuple:
            ret = rc.PASS

    elif test == 'return_object':
        if isinstance(var, TaskData):
            print('var.get_task_name() ' + var.get_task_name())
            ret = rc.PASS


    return ret

