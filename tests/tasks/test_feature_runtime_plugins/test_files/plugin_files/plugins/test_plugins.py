

import os
from krempack.core import plugin
from krempack.common import kremtree

output_dir = kremtree.find_common_dir("output")

def write_output_file(file, input):
    file = open(os.path.join(output_dir, file), 'w')
    file.write(input)
    file.close()
    print("File written: " + str(file))


class TestPluginAllHooks(plugin.Plugin):
    name = "Test-plugin-hooks"

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
            task.get_run_name()
            job.name
            write_output_file("pre_task_execution", "test_line")
        except Exception as e:
            pass

    def job_progress_text(self, task, progress_text):
        try:
            #the first line is to check that we get the task object and not just task name
            task.get_run_name()
            #there should be at least 3 elements in the progress_text list
            write_output_file("job_progress_text", progress_text[2])
        except Exception as e:
            pass

    def pre_task_function_call(self, task):
        try:
            #the first line is to check that we get the task object and not just task name
            task.get_run_name()
            write_output_file("pre_task_function_call", "test_line")
        except Exception as e:
            pass

    def post_task_function_call(self, task):
        try:
            #the first line is to check that we get the task object and not just task name
            task.get_run_name()
            write_output_file("post_task_function_call", "test_line")
        except Exception as e:
            pass

    def post_task_execution(self, task, job):
         try:
             # the first two linea are to check that we get the task and job objects and not just task and job names
             task.get_run_name()
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

class PluginPassData(plugin.Plugin):
    name = "pass-data"

    def __init__(self):
        None

    def job_start(self, job):
        job.set_plugin_data(self.name, "data_to_job_end")

    def pre_task_function_call(self, task):
        task.set_plugin_data(self.name, "data_to_post_task")

    def post_task_function_call(self, task):
        if task.get_plugin_data(self.name) == "data_to_post_task":
            write_output_file("task_data_ok", "test_line")

    def job_end(self, job):
        if job.get_plugin_data(self.name) == "data_to_job_end":
            write_output_file("job_data_ok", "test_line")

class PluginPassDataParallel(plugin.Plugin):
    name = "pass-data-parallel"

    def __init__(self):
        None

    def pre_task_function_call(self, task):
        postfix = task.full_run_nr.split('_')[1]
        task.set_plugin_data(self.name, "data_to_post_task_" + postfix)

    def post_task_function_call(self, task):
        postfix = task.full_run_nr.split('_')[1]
        if task.get_plugin_data(self.name) == "data_to_post_task_" + postfix:
            write_output_file("task_data_ok_" + postfix, "test_line")