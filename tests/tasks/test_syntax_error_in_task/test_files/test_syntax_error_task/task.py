#!/bin/env python
from library.returncodes import *


'''This function has a syntax error'''
def run_with_syntax_error(task):

    prin t("this is a syntax error!")

    #any return code will do since KREM should raise an exception when loading this module
    #and this function should never be called
    return(rc.PASS)

