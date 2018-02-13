#!/bin/env python
import sys
import os
from library.returncodes import *


def test_func(task):
    print("Running test task")
    return(rc.PASS)

