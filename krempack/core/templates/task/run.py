#!/bin/env python
import sys
import os
from library.task import *


_output_path = None

'''
Task data is passed to this function
'''
def setup_task(task):
    global _output_path
    _output_path = task.get_output_path()


def run_without_variables():
    print "executing function 'run_without_variables'"

    '''
    remove the above code if not applicably to your task
    '''


    '''

    Your code here:

    '''



    #return one of the below error codes:
    return(rc.PASS)
    return(rc.FAIL)
    return(rc.SKIP)
    return(rc.UNSTABLE)

def run_with_variable_list(args):

    #get variables passed from job to task
    print "executing function 'run_with_variable_list'"
    print "variables passed from job to task: " + str(args)

    '''
    remove the above code if not applicably to your task
    '''



    '''

    Your code here:

    '''



    #return one of the below error codes:
    return(rc.PASS)
    return(rc.FAIL)
    return(rc.SKIP)
    return(rc.UNSTABLE)

def run_with_named_variables(var1, var2):

    #get variables passed from job to task
    print "executing function 'run_with_named_variables'"
    print "named variables passed from job to task: var1: " + str(var1) + " var2: " + str(var2)

    '''
    remove the above code if not applicably to your task
    '''



    '''

    Your code here:

    '''



    #return one of the below error codes:
    return(rc.PASS)
    return(rc.FAIL)
    return(rc.SKIP)
    return(rc.UNSTABLE)

