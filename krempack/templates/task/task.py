#!/bin/env python
from library.returncodes import *


'''
At least one task function is required
Below are three examples
You may change function names as you wish
'''


'''This function gets no variables from the job'''
def run_without_variables(task):

    print ("executing function 'run_without_variables'")

    '''
    Your code here:
    '''

    #Return codes and defined in library/returncodes.py
    return(rc.PASS)


'''This function gets a single variable from the job'''
def run_with_variable_list(task, args):

    #get variables passed from job to task
    print ("executing function 'run_with_variable_list'")
    print ("variables passed from job to task: " + str(args))

    '''
    Your code here:
    '''

    return(rc.PASS)


'''This function gets multiple named variables from the job'''
def run_with_named_variables(task, var1, var2):

    #get variables passed from job to task
    print ("executing function 'run_with_named_variables'")
    print ("named variables passed from job to task: var1: " + str(var1) + " var2: " + str(var2))

    '''
    Your code here:
    '''

    return(rc.PASS)

