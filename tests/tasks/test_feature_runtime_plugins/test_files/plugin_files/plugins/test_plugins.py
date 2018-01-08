#!/usr/bin/env python

import os
from krempack.core import plugin
from krempack.common import kremtree

output_dir = kremtree.find_common_dir("output")

def write_output_file(file, input):
    file = open(os.path.join(output_dir, file), 'w')
    file.write(input)
    file.close()
    print("File written: " + str(file))


class TestPluginAllEntrypoints(plugin.Plugin):
    name = "Test-plugin-entrypoints"

    def __init__(self):
        None
 
    def job_configuration(self, job):
        write_output_file("job_configuration", "test_line")
    def pre_task_execution(self, task):
        write_output_file("pre_task_execution", "test_line")
    def post_task_execution(self, task):
        write_output_file("post_task_execution", "test_line")
    def post_processing(self, job):
        write_output_file("post_processing", "test_line")

func_call_order=[]
class PluginCalledFirst(plugin.Plugin):
    name = "Test-plugin-called-first"

    def __init__(self):
        None
    def job_configuration(self, job):
        print("Running first plugin")
        func_call_order.append("first")

class PluginCalledSecond(plugin.Plugin):
    name = "Test-plugin-called-second"

    def __init__(self):
        None
    def job_configuration(self, job):
        print("Running second plugin")
        func_call_order.append("second")

class PluginCalledThird(plugin.Plugin):
    name = "Test-plugin-called-third"

    def __init__(self):
        None
    def job_configuration(self, job):
        print("Running third plugin")
        func_call_order.append("third")

class PluginCheckCallOrder(plugin.Plugin):
    name = "check-call-order"

    def __init__(self):
        None
    def post_processing(self, job):
        print("Call order: " + str(func_call_order))
        if func_call_order[0] != "first" or func_call_order[1] != "second" or func_call_order[2] != "third":
            print("ERROR: Plugin call order not as expeted.")
        else:
            write_output_file("call_order_ok", "test_line")
