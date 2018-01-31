

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
 
    def job_start(self, job):
        try:
            # the first line is to check that we get the job object and not just task name
            job.name
            write_output_file("job_start", "test_line")
        except Exception as e:
            pass

    def pre_task_execution(self, task, job):
        try:
            #the first two linea are to check that we get the task and job objects and not just task and job names
            task.get_task_name()
            job.name
            write_output_file("pre_task_execution", "test_line")
        except Exception as e:
            pass


    def pre_task_function_call(self, task):
        try:
            #the first line is to check that we get the task object and not just task name
            task.get_task_name()
            write_output_file("pre_task_function_call", "test_line")
        except Exception as e:
            pass


    def post_task_function_call(self, task):
        try:
            #the first line is to check that we get the task object and not just task name
            task.get_task_name()
            write_output_file("post_task_function_call", "test_line")
        except Exception as e:
            pass

    def post_task_execution(self, task, job):
         try:
             # the first two linea are to check that we get the task and job objects and not just task and job names
             task.get_task_name()
             job.name
             write_output_file("post_task_execution", "test_line")
         except Exception as e:
             pass

    def job_end(self, job):
        try:
            # the first line is to check that we get the job object and not just task name
            job.name
            write_output_file("job_end", "test_line")
        except Exception as e:
            pass

func_call_order=[]
class PluginCalledFirst(plugin.Plugin):
    name = "Test-plugin-called-first"

    def __init__(self):
        None
    def job_start(self, job):
        print("Running first plugin")
        func_call_order.append("first")

class PluginCalledSecond(plugin.Plugin):
    name = "Test-plugin-called-second"

    def __init__(self):
        None
    def job_start(self, job):
        print("Running second plugin")
        func_call_order.append("second")

class PluginCalledThird(plugin.Plugin):
    name = "Test-plugin-called-third"

    def __init__(self):
        None
    def job_start(self, job):
        print("Running third plugin")
        func_call_order.append("third")

class PluginCheckCallOrder(plugin.Plugin):
    name = "check-call-order"

    def __init__(self):
        None
    def job_end(self, job):
        print("Call order: " + str(func_call_order))
        if func_call_order[0] != "first" or func_call_order[1] != "second" or func_call_order[2] != "third":
            print("ERROR: Plugin call order not as expeted.")
        else:
            write_output_file("call_order_ok", "test_line")
