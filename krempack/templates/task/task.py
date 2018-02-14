#!/bin/env python
from library.returncodes import *


'''
At least one task function is required
Below are three examples
You may change function names as you wish
'''


'''This function gets no arguments from the job'''
def run_without_arguments(task):

    print ("executing function 'run_without_arguments'")

    '''
    Your code here:
    '''

    #Return codes and defined in library/returncodes.py
    return(rc.PASS)


'''This function gets a single argument from the job'''
def run_with_argument_list(task, args):

    #get arguments passed from job to task
    print ("executing function 'run_with_argument_list'")
    print ("arguments passed from job to task: " + str(args))

    '''
    Your code here:
    '''

    return(rc.PASS)


'''This function gets multiple named arguments from the job'''
def run_with_named_arguments(task, arg1, arg2):

    #get arguments passed from job to task
    print ("executing function 'arguments'")
    print ("named arguments passed from job to task: arg1: " + str(arg1) + " arg2: " + str(arg2))

    '''
    Your code here:
    '''

    return(rc.PASS)

