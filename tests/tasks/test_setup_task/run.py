#!/bin/env python
import os

from library.task import *


_output_path = None

def setup_task(task):    
    global _output_path
    _output_path = task.get_output_path()


def run():
    global _output_path

    if _output_path is None:
        result = rc.FAIL
    else:
        result = rc.PASS
        print(_output_path)


    return(result)

