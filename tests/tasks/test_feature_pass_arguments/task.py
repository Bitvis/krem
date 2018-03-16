#!/bin/env python
import sys
import os
from library.returncodes import *
from library.testlib import parameters as p


def run_argument_single(task, test_arg):
    result = rc.UNSTABLE
    print("Expected argument: " + str(p.test_arg_1))
    print("arguments passed from job to task: " + str(test_arg))

    if test_arg is None:
        print("ERROR: No arguments passed from job to task")
        result = rc.FAIL
    elif test_arg != p.test_arg_1:
        print("ERROR: argument list passed from job to task is not as expected")
        result = rc.FAIL
    else:
        print("argument list passed from job to task OK")
        result = rc.PASS

    return result



def run_argument_list(task, test_arg_list):

    result = rc.UNSTABLE
    print("Expected argument list: " + str(p.test_arg_list))
    print("arguments passed from job to task: " + str(test_arg_list))
    
    if test_arg_list is None:
        print("ERROR: No arguments passed from job to task")
        result = rc.FAIL
    elif test_arg_list != p.test_arg_list:
        print("ERROR: argument list passed from job to task is not as expected")
        result = rc.FAIL
    else:
        print("argument list passed from job to task OK")
        result = rc.PASS
        
    return result
        
def run_named_arguments(task, test_arg_1, test_arg_2):

    result = rc.PASS
    
    print("Expected arguments:")
    print("test_arg_1: "+ str(p.test_arg_1))
    print("test_arg_2: "+ str(p.test_arg_2))
    print("arguments passed from job to task:")
    print("test_arg_1: "+ str(test_arg_1))
    print("test_arg_2: "+ str(test_arg_2))

    if test_arg_1 is None:
        print("ERROR: test_arg_1 is empty")
        result = rc.FAIL
    elif test_arg_1 != p.test_arg_1:
        print("ERROR: test_arg_1 does not match expected")
        result = rc.FAIL
    
    if test_arg_2 is None:
        print("ERROR: test_arg_2 is empty")
        result = rc.FAIL
    elif test_arg_2 != p.test_arg_2:
        print("ERROR: test_arg_2 does not match expected")
        result = rc.FAIL
    
    if not result:
        print("arguments passed from job to task OK")
        result = rc.PASS
        
    return result


def run_with_argument_dict(task, **args):

    print ("executing function 'run_with_argument_dict'")

    result = rc.FAIL
    if type(args) is dict:
        if args == p.test_arg_dict:
            print("arguments passed from job to task OK")
            print(str(args))
            result = rc.PASS

    if result == rc.FAIL:
        print("ERROR: expected dictionary")


    return(result)


def run_with_argument_int(task, args):

    print ("executing function 'run_with_argument_int'")

    result = rc.FAIL
    if type(args) is int:
        if args == p.test_arg_int:
            print("arguments passed from job to task OK")
            print(str(args))
            result = rc.PASS

    if result == rc.FAIL:
        print("ERROR: expected int")

    return(result)


def run_with_argument_float(task, args):

    print ("executing function 'run_with_argument_float'")

    result = rc.FAIL
    if type(args) is float:
        if args == p.test_arg_float:
            print("arguments passed from job to task OK")
            print(str(args))
            result = rc.PASS

    if result == rc.FAIL:
        print("ERROR: expected float")

    return(result)