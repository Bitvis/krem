#!/bin/env python
from library.returncodes import *


'''
At least one task function is required
Below are three examples
You may change function names as you wish
'''


'''This function gets no arguments from the job'''
def run_without_arguments(task):

    print("executing function 'run_without_arguments'")

    '''
    Your code here:
    '''

    # Return codes and defined in library/returncodes.py
    return(rc.PASS)


'''This function gets a single argument or a list from the job'''
def run_with_single_argument(task, args):

    # get argument passed from job to task
    print("executing function 'run_with_single_argument'")
    print("arguments passed from job to task: " + str(args))

    # prints either first element in list or first character in string
    print(args[0])

    '''
    Your code here:
    '''

    return(rc.PASS)

'''This function gets a dictionary from the job'''
def run_with_argument_dict(task, **args):

    # get arguments passed from job to task
    print("executing function 'run_with_argument_dict'")
    print("dictionary passed from job to task: " + str(args))

    '''
    Your code here:
    '''

    return(rc.PASS)


'''This function gets multiple named arguments from the job'''
def run_with_named_arguments(task, arg1, arg2):

    # get arguments passed from job to task
    print("executing function 'arguments'")
    print("named arguments passed from job to task: arg1: " + str(arg1) + " arg2: " + str(arg2))

    '''
    Your code here:
    '''

    return(rc.PASS)

