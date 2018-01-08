#!/bin/env python
import sys
import os
import subprocess
import re

from library.task import *
from library.testlib import parameters as p

def compare_lists(list_to_verify, list2):
    missing_from_list = []
    
    for item in list2:
        if not item in list_to_verify:
            missing_from_list.append(item)
            
    return missing_from_list

def shell_run(cmd, print_enable=True):
    output = []
    print("SHELL CMD: '" + str(cmd) + "'")
    cmd_list = cmd.split()
    out = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw_output = out.communicate()
    output.append(raw_output[0].decode('utf-8'))
    output.append(raw_output[1].decode('utf-8'))

    if out.returncode != 0:
        print("ERROR: Cmd '" + str(cmd) + "' failed.")
        print(str(output[1]))
        
    if print_enable:
        stdout = output[0].replace("\n", "\n*\t")
        stderr = output[1].replace("\n", "\n*\t")
        print("SHELL STDOUT:")
        print("*\t" + str(stdout))
        print("SHELL STDERR:")
        print("*\t" + str(stderr))
   
    return (out.returncode, output[0], output[1])

def find_output_job_instance(output_job_path):
    job_instance = None
    result = rc.PASS
    try:
        print("Searching " + str(output_job_path) + " for job instance")
        for dir in os.listdir(output_job_path):
            m = re.search(p.TIMESTAMP_REGEX, dir)
            if m:
                if job_instance is not None:
                    print("WARNING: Multiple job instance output directories found. Attempting to use: " + str(job_instance))
                    result = rc.UNSTABLE
                    break
                else:
                    job_instance = os.path.basename(dir)
                    print("job_instance = " + str(job_instance))
    except EXCEPTION:
        print("Unable to find job instance in output directory. Abort test.")
        result = rc.FAIL
        
    return (result, job_instance)

def check_file_content(file_path, expected_content_list):
    result = rc.PASS
    if not os.path.isfile(file_path):
        result = rc.FAIL
        print("ERROR: File not found: " + str(file_path))
    elif os.path.getsize(file_path) == 0:
        result = rc.FAIL
        print("ERROR: empty file: " + str(file_path))
    else:
        file = open(file_path, 'r')
        file_string = ""
        for line in file:
            file_string = file_string + line
        for line in expected_content_list:
            if line not in file_string:
                result = rc.FAIL
                print("ERROR: line '" + str(line) + "' not found in file '" + str(file_path) + "'")
        if not result:
            print("File '" + str(file_path) + "' OK")
    
    return result

