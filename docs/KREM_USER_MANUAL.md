## KREM User Manual

#### About KREM

**KREM**  is a **very lightweight automation framework**.  **KREM**  is also suitable for testing.  **KREM**  runs jobs made up of tasks executed in sequence, in parallel or a combination of both.

**KREM**  is written in Python, but can execute scripts and programs written in any language.

We are continuously improving  **KREM**. We want to keep  **KREM as**  lightweight and compact as possible, at the same time allowing extended functionality through a plugin interface.

We will provide some plugins, but anyone is more than welcome to contribute.


<font color=green>KREM support Python 2.7 and 3.6 in Linux.</font>
<p><font color=green>KREM in Windows is supported in Git Bash and Cygwin.</font>





# Table of Contents
[Quick Start Guide](#quick-start-guide)

[Tutorials](#tutorials)

* [Installing KREM](#installing-krem)

* [KREM selftest](#krem-selftest)

* [Basic tutorial](#basic-tutorial)

[Technical Reference](#technical-reference)

* [Project](#project)

* [Job](#job)

* [Task](#task)

* [Plugins](#plugins)

* [Advanced features](#advanced-features)


[FAQ](#faq)

[Troubleshooting](#troubleshooting)

[License](#license)

[Change log](#change-log)


## Quick Start Guide

##### get KREM
```
git clone https://github.com/Bitvis/krem.git
```

**install KREM**

```
python ./krem/install.py
source ~/.bashrc
```

**create a project**

```
krem init –p project_foo
cd project_foo
```

**create a job**

```
krem init –j job_foo
```

**create a task**

```
krem init –t task_foo
```

**run the job**

```
krem run –j job_foo
```

**list jobs**

```
krem list –j
```

**list tasks**

```
krem list –t
```


# Tutorials

## Installing KREM

### Linux

As mentioned in the [Quick Start Guide](#quick-start-guide), KREM is installed by running:

```
git clone https://github.com/Bitvis/krem.git

python ./krem/install.py
source ~/.bashrc
```

In case the `install.py` fails and _krem_ is not in your PATH environment variable, you can add the following two lines to your _~/.bashrc_ file.

```
export PATH=<krem path>:$PATH
export PYTHONPATH=<krem path>:<krem installation>/krempack:$PYTHONPATH
```
### Windows

#### Gitbash

Install Git Bash from: https://gitforwindows.org and follow the instructions from [Linux installation](#linux) section. 



#### Cygwin

Download Cygwin from https://www.cygwin.com and select python2 or python3 interpreter package in the installation. Follow the instructions from [Linux installation](#linux) section. 



## KREM selftest

KREM comes with a selftest project. The test project is located in _\<krem path\>/tests_. To execute selftest run:

```
cd <krem path>/tests
krem run -j integration_testing
```

KREM is installed correctly if all tests pass.


## Basic tutorial
#### Creating a project

Before you can start using KREM you must create a project. You can create as many projects as you want in any location.

To create a project _project_foo_, run:

```
$ krem init -p project_foo
$ cd project_foo
```

A directory _project_foo_ is created.

For more information on project directories see [Project](#project).

#### Creating a job

To create an example job _job_foo_, run:

```
$ krem init -j job_foo
```

This command will create a job directory _jobs/job_foo_ and place a template file _job.py_ in the directory.

#### Creating a task

To create an example task _task_foo_, run:

```
$ krem init -t task_foo
```

This will create a task directory _tasks/task_foo/_ and place a template file _task.py_ and _\_\_init\_\_.py_ in the directory.

#### Running a job

To execute the example job created above, run:

```
$ krem run -j job_foo
```

The job name in the above command can be replaced with a job number. All jobs and the corresponding job numbers can be listed by running:

```
$ krem list -j

        Available jobs:

[nr]        name
[0]        job_foo
```


All available jobs are listed with a job number to the left of the job name.
In this case there is only one job.

To run the _job_foo_ by job number, run:

```
$ krem run -j 0
```

#### Job progress

While KREM executes a job, it will output progress to the terminal. Job progress is also referred to as
job logging. An example progress is shown below.

```
[INFO]: 1_1     task_foo  run_without_arguments  []
[INFO]: 2_1     task_foo  run_with_argument_list  ['argument passed from job', 'as list']
[INFO]: 3_1     task_foo  run_with_named_arguments  [('arg1', 'arg1_value'), ('arg2', 'arg2_value')]
[INFO]: 4_1     task_foo  run_with_named_arguments  [('arg1', ''), ('arg2', 'run_in_parallel')]
[INFO]: 4_2     task_foo  run_with_named_arguments  [('arg1', 'also'), ('arg2', 'run_in_parallel')]
```

##### Job progress components

| | |
| --- | --- |
| log level | Log level for current line. There are four log levels: DEBUG, RESET, WARN and ERROR For more information see [Job logging](#job-logging)|
| run number | Run number consists of two integers separated with an underscore. The first integer starts at '1' and is incremented for each serial task started. The second integer is always '1' for serial tasks. For parallel tasks, the first integer is the same for all tasks run in the same parallel batch, while the second integer is incremented for each parallel task started in the current batch. |
| task name | Name of the executed task |
| task function name | Name of the called task function |
| task arguments | Task arguments are arguments passed from a job to a task function. A list of arguments follows the task function where arguments are passed from a job to a task function. |

#### Results report

Upon completion of all tasks KREM outputs a results report. An example report is shown below.
The report lists all tasks with the corresponding results in the same order as they were run.
Note the run number in front of each task for cross-reference .

```
        TASK       FUNCTION                      RESULT
1_1     task_foo   run_without_arguments         PASS
2_1     task_foo   run_with_argument_list        PASS
3_1     task_foo   run_with_named_arguments      PASS
4_1     task_foo   run_with_named_arguments      PASS
4_2     task_foo   run_with_named_arguments      PASS

SUMMARY:
ERROR                0
EXCEPTION            0
FAIL                 0
PASS                 5
SKIPPED              0
SUCCESS              0
UNSTABLE             0
```

#### Output files

First time a job is run, a new directory for that job is created in the _output_ directory.
For each execution of the same job a directory with a timestamp is created.
A symbolic link _latest_ is created pointing at the latest timestamped directory.
<font color=red>Note that the symbolic link is not created in Windows.</font>
The _info_ file is not relevant for this tutorial.

KREM will write job progress, as output to the terminal, to _output/\<job name\>/latest/execution.log_.
KREM will also write job results report to _output/\<job name\>/latest/results_.

Change to _output_ directory and list all entries:

```
$ cd output
$ ls -l

-rw-rw-r-- 1 mk mk   35 feb.   9 14:45 info
drwxrwxr-x 3 mk mk 4096 feb.   9 14:45 job_foo
```

Now change to _job_foo_ and list all entries:

```
$ cd job_foo
$ ls -l

drwxrwxr-x 7 mk mk 4096 feb.   9 14:45 20180209_144547
lrwxrwxrwx 1 mk mk   15 feb.   9 14:45 latest -> 20180209_144547
```

Finally, change to the _latest_ _directory:_

```
$ cd latest
$ ls -l

drwxrwxr-x 2 mk mk 4096 feb.   9 14:45 1_1_task_foo_run_without_arguments
drwxrwxr-x 2 mk mk 4096 feb.   9 14:45 2_1_task_foo_run_with_argument_list
drwxrwxr-x 2 mk mk 4096 feb.   9 14:45 3_1_task_foo_run_with_named_arguments
drwxrwxr-x 2 mk mk 4096 feb.   9 14:45 4_1_task_foo_run_with_named_arguments
drwxrwxr-x 2 mk mk 4096 feb.   9 14:45 4_2_task_foo_run_with_named_arguments

-rw-rw-r-- 1 mk mk  407 feb.   9 14:45 execution.log
-rw-rw-r-- 1 mk mk  499 feb.   9 14:45 results
-rw-rw-r-- 1 mk mk 1035 feb.   9 14:45 tasks.log
```

There are the two files mentioned above, _execution.log_ and _results_.
The task log file _tasks.log_ is explained later in this tutorial.
There are also separate directories for each task.
These directories are the task output directories.
KREM will not care about the content of the task output directories so a task is free to write any files to its output directory.

#### Task log

All output from all tasks is continuously written to _output/\<job name\>/latest/tasks.log_.

The text below is a part of an example _tasks.log_ file. Note that each line is prefixed with the task run number
to which the output belongs to. The lines containing _\*\*\* Task start..._ and _\*\*\* Task end..._ are inserted by KREM.


```
1_1  *** Task start:   task_foo  run_without_arguments ***
1_1  executing function 'run_without_arguments'
1_1  *** Task end: task_foo ***

2_1  *** Task start:   task_foo  run_with_argument_list ***
2_1  executing function 'run_with_argument_list'
2_1  arguments passed from job to task: ['argument passed from job', 'as list']
2_1  *** Task end: task_foo ***
```



# Technical Reference

## Project

Each project is contained in a separate directory.
KREM automatically populates project directories with subdirectories as shown below.


| Directory | Description |
| --- | --- |
| config | Feel free to add any configuration files for your project here. KREM does not care about the content of this directory. |
| jobs | This is where all your jobs are located. There is a subdirectory in _jobs_ for each job. |
| output | All output such as logs, results reports and any custom files saved by tasks ends up here. |
| library | This directory contains python modules to be used in your jobs and tasks. This is also where we advise to put all your plugins. For plugins see [Plugins](#plugins). |
| tasks | You will find all your tasks in this directory. There is a subdirectory in _tasks_ for each task. |

## Job

This section will show you how to implement jobs.
For information on how to create and run jobs see [Basic tutorial](#basic-tutorial).

### Job examples

#### Serial job example

A job file _job.py_ must contain at least the following code:

```python
from krempack.core import kjob
from library.returncodes import *

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)
    job.start()

    err = job.run_task_serial('task_foo', 'task_function_foo')

    job.end()
    exit(err)
```

First, a job object must be created by calling function `kjob.Job()`.
The `rc` argument is short for return codes and is imported from _library.returncodes_.
More on return codes later in this section and also in [Task](#task).

Function `job.start()` initializes the job. For instance, logging is initialized here.

After a job is initialized it is time to add tasks.
The above example executes a single task `task_foo` with a task function `task_function_foo`.
Once the function `run_task_serial()` is called KREM will execute the task by calling its task function.

Any return code returned from a task function will be returned by `run_task_serial()`.
There is an exception to the this rule.
If an exception is raised within the task and is not caught by the task,
then KREM will catch the exception and `run_task_serial()` will return `rc.EXCEPTION` back to the job.

Finally, when all the tasks have been executed, the function `job.end()` must be called.
This function generates the results report.

#### Parallel job example

The below example shows how tasks can be executed in parallel.

```python
job.run_task_parallel('task_foo', 'task_function_foo')
job.run_task_parallel('task_foo', 'task_function_foo')

task_results = job.wait_for_complete()
```

A batch of parallel tasks can have any number of tasks and has to be followed by a call to function
`job.wait_for_complete()`. `job.wait_for_complete()` blocks until all parallel tasks finish executing.
`job.wait_for_complete()` returns a list of return codes for all parallel tasks.
Return codes are in the same order as the order of which the tasks are added.

#### A mixed job example

The following example shows how a job can execute both serial and parallel tasks.

```python
job.start()

job.run_task_serial('task_foo', 'task_function_foo')

job.run_task_parallel('task_foo', 'task_function_foo')
job.run_task_parallel('task_foo', 'task_function_foo')
job.wait_for_complete()

job.run_task_serial('task_foo', 'task_function_foo')

job.end()
```

### Conditional statements and loops

It is often necessary to react to task return codes.
This is easily achieved by using conditional statements.
Executing the same task multiple times can be done in loops. Some examples follow:

```python
err = job.run_task_serial('power', ' power_on')

if err == rc.PASS:
    job.run_task_serial('motor', ' start')
else:
    job.run_task_serial('power', ' power_off')

for i in range(10):
    err = job.run_task_serial('network', 'ping', arguments="192.168.1.1")

    if err == rc.PASS:
        break
```

### Task result handling

As mentioned in [Job examples](#job-examples), function `job.wait_for_complete()`
returns return codes from all the parallel tasks in a parallel batch.
To get return codes from all tasks in a job, both serial and parallel, executed up to a given point call
function `job.get_task_results()`.

```python
all_task_results = job.get_task_results()
```

### Passing arguments

You will soon come to a point where you want to pass arguments to task functions.
You can pass single arguments, lists, dictionaries and named arguments to task functions.
For corresponding task functions implementations see the [Task](#task).
The following are some examples.


#### No arguments

The following is an example on how to execute tasks where the function require no arguments.

```python
job.run_task_serial('motor, 'power_on')
job.run_task_parallel('motor, 'power_on')
```

#### Single argument

The following is an example on passing a single argument to the task function _power_.

```python
job.run_task_serial('motor, 'power', arguments="on")
job.run_task_parallel('motor, 'power', arguments="on")
```
or alternatively

```python
turn_power = "on"
job.run_task_serial('motor, 'power', arguments=turn_power)
job.run_task_parallel('motor, 'power', arguments=turn_power)
```


#### List

The following is an example on passing a list argument to the task function _power_.

```python
job.run_task_serial('motor, 'power', arguments=["on", "off"])
job.run_task_parallel('motor, 'power', arguments=["on", "off"])
```
or alternatively

```python
turn_power = ["on", "off"]
job.run_task_serial('motor, 'power', arguments=turn_power)
job.run_task_parallel('motor, 'power', arguments=turn_power)
```

#### Named arguments

The following is an example on passing named arguments to the task function _power_.

```python
job.run_task_serial('motor, 'power', arguments[("turn", "on"), ("rpm", 1000)])
job.run_task_parallel('motor, 'power', arguments=[("turn", "on"), ("rpm", 1000)])
```
or alternatively

```python
turn_power = {"on":1000,'off':2000}
job.run_task_serial('motor, 'power', arguments=turn_power)
job.run_task_parallel('motor, 'power', arguments=turn_power)
```

#### Dictionary

The following is an example on passing a dictionary argument to the task function _power_.

```python
job.run_task_serial('motor, 'power', arguments={"on":1000,'off':2000})
job.run_task_parallel('motor, 'power', arguments={"on":1000,'off':2000})
```
or alternatively

```python
turn_power = {"on":1000,'off':2000}
job.run_task_serial('motor, 'power', arguments=turn_power)
job.run_task_parallel('motor, 'power', arguments=turn_power)
```


### Job logging
In KREM, the terms 'job logging' and 'job progress' are interchangeable.
Job logging is output to the terminal and written to _execution.log_
as mentioned in [Output files](#output-files).

For an example of job progress see [Job progress](#job-progress).

There are four job log levels: _debug_, _info_, _warn_ and _error_.
The example in [Job progress](#job-progress) shows progress with log level set to _info_,
which is the default.
You can change job log level anywhere between `job = kjob.Job(__file__, rc)` and `job.end()` and you can change it
as many times as you wish.
<p>The below is an example on changing the job log level to 'debug'

```python
job.start()

job.config.job_logger.set_log_level('debug')

job.end()
```

## Task

This section will show you how to implement tasks.
You are advised to read through the [Basic tutorial](#basic-tutorial) and [Job](#job) first.

### Task example

A task file task.py must contain at least the following code:

```python
from library.returncodes import *

def run_without_arguments(task):
    '''
    Your code here:
    '''
    return(rc.PASS)
```

The function `run_without_arguments()` is a task function to be executed from a job. You can name a
task function as you like.

<p>You can add as many task functions to a task as you like. You can also add functions not to be used
as task functions, but to be called from the task functions.
<p>A task must return a return code imported from _library.returncodes_ as `rc`.

The `task` argument is mandatory for all task functions as KREM prepends the `task` argument to the
task function argument list.

`task` is an object with information on the current task as follows:
<br> _task_name_:the current task name
<br> _run_name_: the current task name including the run number and current task function
<br> _run_nr_: run number of the current task. For more information on run numbers see [Job progress components](#job-progress-components).
<br> _full_run_nr_: full run number of the current task.
<br> _job_output_path_: path to the current job directory in the output directory
<br> _output_path_: path to the current task directory in the output directory.
This is where you can save files from your task if applicable.

The following `task` getter functions return the above properties:

```python
def get_task_name(self):
def get_run_name(self):
def get_run_nr(self):
def get_full_run_nr(self):
def get_job_path(self):
def get_output_path(self):
```

The `task` object also provides several setter functions.
These function shall not be called by the task.


### Task function arguments

You can pass arguments from jobs to task functions. The following shows how to implement task functions
with arguments. How to pass arguments from a job to a task function is shown in [Passing arguments](#passing-arguments)

#### Single argument

The following is an example on a task function _power_ with a single argument.
Note that since the `task` argument is prepended by KREM and is not an user argument
it is not counted in this context.

```python
def power(task, turn):
    motor(turn)
    return rc.PASS
```

#### List

The following is an example on a task function _power_ with a list argument.

```python
def power(task, turn_list):
    for turn in turn_list:
        motor(turn_list[turn])
    return rc.PASS
```

#### Named arguments

The following is an example on a task function _power_ with named arguments.

```python
def power(task, turn="off", rpm):
    motor(turn, rpm)
    return rc.PASS
```

#### Dictionary

The following is an example on a task function _power_ with a dictionary argument.

```python
def power(task, turn_dict):
    motor("on", rpm = turn_dict["on"]
    motor("off", rpm = turn_dict["off"]
    return rc.PASS
```

## Plugins

Runtime plugins provide additional functionality to jobs and tasks.

CLI plugins provide additional commands and arguments to the KREM command-line interface.

### Adding plugins

The following instructions shows how to enable plugins in your jobs.
You can implement your own plugins or you can use existing plugins implemented by Bitvis.

#### Get plugins

Clone the _krem_plugins_ repository directly into _\<krem_project\>/library/plugins_.

```
$ git clone https://github.com/Bitvis/krem_plugins.git
```

 The plugin you will now add to your jobs is implemented
 in _\<krem_project\>/library/plugins/krem_plugins/print_task_results/print_task_results.py_.

#### Enabling plugin in project

The following will make the plugin available to all jobs in the project.

Enable the plugin in the plugin setup function located in _\<krem_project\>/library/setup.py_.
This file must contain the following:

```python
from krempack.core import plugin
from library.plugins.krem_plugins.print_task_results import print_task_results
from library.plugins.krem_plugins.verify_jobs import verify_jobs

def setup_plugins(plugin_handler):
    plugin_handler.register_plugin(print_task_results.PluginPrintTaskResults)

def setup_cli_plugins(plugin_handler):
    plugin_handler.register_plugin(verify_jobs.PluginVerifyJobs)
```

where setup_plugins is used for registering runtime plugins, and setup_cli_plugins is used for
registering CLI plugins.

PluginPrintTaskResults and PluginVerifyJobs are classes, located in _print_task_results.py_ and _verify_jobs.py_ respectively. 
Adding additional plugins is done in the same way as above.

No further action is required for enabling CLI plugins after they have been registered. 

#### Enabling plugins in jobs

Import setup_plugins and call the `setup_plugins()` function from a job.
`setup_plugins()` must be called before `job.start()`.

```python
from library.setup import *

if __name__ == '__main__':

    job = kjob.Job(__file__, rc)

    setup_plugins(job.plugin_handler)

    job.start()
```

#### Plugin execution order

For every hook, all registered plugins that has implemented the target hook function will be executed one after the other. Unless specified, the execution order is random. The execution order for each plugin in each hook can be configured in the functions _setup\_plugins()_ and _setup\_cli\_plugins()_. The example below shows how the execution order is configured for the hook _pre\_task\_function\_call_.

```python
def setup_plugins(plugin_handler):
    plugin_handler.register_plugin(PluginA)
    plugin_handler.register_plugin(PluginB)
    plugin_handler.register_plugin(PluginC)
    plugin_handler.register_plugin(PluginD)

    plugin_handler.hooks["pre_task_function_call"].append_first_to_execute(PluginA)
    plugin_handler.hooks["pre_task_function_call"].append_first_to_execute(PluginB)

    plugin_handler.hooks["pre_task_function_call"].append_last_to_execute(PluginC)
    plugin_handler.hooks["pre_task_function_call"].append_last_to_execute(PluginD)
```
For the hook _pre\_task\_function\_call_, the execution order will be: _PluginA_, _PluginB_, _PluginC_, then _PluginD_. Any other registered plugins with an implemented function for _pre\_task\_function\_call_ will be called somewhere in between _PluginB_ and _PluginC_, with no specific order. 

Check the _README.md_ file, provided with each plugin, to see if it requires a specific order of execution for any of the hooks. 

### Plugin interface

This section is intended for plugin developers.

#### Task and job plugins

A plugin must implement at least one of the below functions.

##### job_start()

Function `job_start()` is called at the beginning of a job.

```python
def job_start(self, job):
```

##### pre_task_execution()

Function `pre_task_execution()` is called just before a task is executed.

```python
def pre_task_execution(self, task, job):
```

##### job_progress_text()

Function `job_progress_text` is called just before the progress is output to the terminal.

```python
def  job_progress_text(self,task, progress_text)
```

##### pre_task_function_call()

Function `pre_task_function_call()` is called just before a task function is called.

```python
def pre_task_function_call(self, task):
```

##### post_task_function_call()

Function `post_task_function_call()` is called right after a task function has returned.

```python
def post_task_function_call(self, task):
```

##### post_task_execution()

In case of serial tasks, function `post_task_execution()` is called after a task has been executed
and the task result is ready.
In case of parallel tasks, this function is called from the `wait_for_complete()` function when all
parallel tasks have finished.

```python
def post_task_execution(self, task, job):
```

##### job_end()

Function `job_end()` is called at the end of a job.

```python
def job_end(self, job):
```

#### CLI plugins

##### cli_commands()

Function `cli_commands()` is used for adding additional commands to KREM. Add path to target command script to the 'commands' dictionary, with the executable name of the command as the key.

```python
# Example from 'help-docs' plugin
def cli_commands(self, commands):
    commands["help"] = os.path.join(os.path.dirname(__file__), "help_cmd.py")
```

##### cli_\<cmd\>_setup_arguments()

Function `cli_<cmd>_setup_arguments()` is used for adding additional arguments to the original KREM commands, where _\<cmd\>_ is the name of the command, eg. `cli_init_setup_arguments()`. The `parser` input variable is of type argparse.ArgumentParser() from the argparse library. To add arguments to the existing command, create a new argument group and add the desired arguments.

```python
# Example from "task_lister" plugin
def cli_list_setup_arguments(self, parser):
    group = parser.add_argument_group()
    group.add_argument("--job-tasks", nargs=1, help="Lists tasks used in target job")
```

##### cli_\<cmd\>_execute_arguments_pre_cmd()

Function `cli_<cmd>_execute_arguments_pre_cmd()` is executed before the inherent functionality of the target _\<cmd\>_ is executed, where _\<cmd\>_ is the name of the command, eg. `cli_init_execute_arguments_pre_cmd()`. The `args` input variable are all arguments passed when calling the command. 

```python
# Example from "task_lister" plugin
def cli_list_execute_arguments_pre_cmd(self, args):
    if args.job_tasks is not None:
        task_lister.run(args.job_tasks[0])
```

##### cli_\<cmd\>_execute_arguments_post_cmd()

Function `cli_<cmd>_execute_arguments_post_cmd()` is executed after the inherent functionality of the target _\<cmd\>_ has been executed, where _\<cmd\>_ is the name of the command, eg. `cli_init_execute_arguments_pre_cmd()`. The `args` input variable are all arguments passed when calling the command.

```python
def cli_list_execute_arguments_post_cmd(self, args):
```

# Advanced features

## Returning variables from tasks to jobs

So far you have been working with task functions returning return codes only.
It is also possible to return additional variables. You can return any type of variable in any
number and combination.

#### Variables from serial tasks

To return variables from tasks executed serially append the variables
to the return statement as shown in the example below:

```python
def return_variables(task):
    var = "return me too"
    var_list = ["return", "me", "too"]
    var_dict = {'return': 1, 'me': 2, 'too': 3}
    return rc.PASS, var, var_list, var_dict
```

To receive the variables in a job do as shown in the example below:

```python
ret, var, var_list, var_dict = job.run_task_serial('task_foo', 'return_variables')

print(var)
print(var_list)
print(var_dict)
```

#### Variables from parallel tasks

To return variables from tasks executed in parallel, append the variables
to the return statement as shown in [Variables from serial tasks](#variables-from-serial-tasks).

To receive variables from tasks executed in parallel do as follows:

```python
job.run_task_parallel('task_foo', 'return_single_variable')
job.run_task_parallel('task_foo', 'return_list_variable')
job.run_task_parallel('task_foo', 'return_object')

return_codes, return_vars = job.wait_for_complete()

# get variables from the first parallel task above
print(return_vars[0])
```

# FAQ

#### Can I have more than one job in the same project?
Yes, you can create as many jobs as you want?

#### Can I add the same tasks to several jobs?
Yes, the same tasks can be added to several jobs.
It is recommended to write tasks in such a way that they can be reused in more than one job.

#### Can the job abort if one of the tasks fail?
It's up to you. All tasks returns a return code (directly from `job.run_task_serial()` or from
`job.wait_for_complete()` for parallel tasks).
Let your job check the return code from the tasks to see if job execution should continue or not.

#### Can I copy my project to other locations or even to other machines?
Yes, as long as you copy the whole directory structure. Make sure to delte all .pyc files after copying to the new location.

#### Can I copy my jobs and tasks to other projects?
Yes. Remember to also copy modules and plugins, from the _library_ directory,
used by your jobs and tasks. Make sure to delte all .pyc files after copying to the new location.

#### Can I copy my plugins to other locations or even to other machines?
Yes, as long as you copy the whole directory structure. Make sure to delte all .pyc files after copying to the new location.

#### How do I uninstall KREM?
Simply remove the KREM directory.
There are no KREM related files placed anywhere except in the KREM directory.
You may also want to remove the path to KREM from the environment variables _PATH_ and _PYTHONPATH_
 and from your file _~/.bashrc_ file.

#### How do I rename or remove a task or job?
KREM recognize tasks and jobs by their directory as they appear in _\<krem_project\>/tasks_
and _\<krem_project\>/jobs_. Simply rename or remove the task or job directory.

# Troubleshooting

#### I keep getting the following error task for all KREM commands:

```python
'ERROR: Project task root directory not found.'
```

You must run _krem_ from within your project directory.
KREM recognizes a project directory by the presence of the following directories:

_'config  library  output  jobs  tasks'_

Make sure that all of the above directories are present in your project directory.
Sometimes the user deletes the _output_ directory to clean up all logs and results.
Simply recreate the directory and try again:

```
$ mkdir output
```


For more information on project directory see [Project](#project).

#### My task calls a sub process. The output from the sub process is printed to the terminal instead of the task log. How can I log the output from the sub process to the task log?

You must direct stdout and stderr from the sub process to the task log.
Stdout and stderr for the task itself have already been directed to the task log.
However, when a sub process is called, stdout and stderr will be by default sent to the terminal.

An example solution is shown below:

```python
import subprocess
import shlex

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode('utf-8'))
    rc = process.poll()
    return rc


task_function(task):

    ret = run_command("<your command here>")
```

#### Job execution stops abruptly with no error messages.

Check if there are any calls to `exit()` in the tasks executed by your job. If `exit()`
is called from a task, the job will exit immediately.
Simply replace any calls to `exit()` with `return(<error code>)`.

#### I keep getting the following error:

```python
[ERROR]: Traceback (most recent call last):
  File "/home/mk/Projects/krem/krempack/core/taskaction.py", line 119, in run_method
    returncode = target_function(task_data)
TypeError: run_without_arguments() takes 0 positional arguments but 1 was given
```
The function `run_without_arguments()` is missing the required _task_ argument.

Add the _task_ argument to `run_without_arguments()` as follows:

```python
def run_without_arguments(task):
```

# License

Copyright (C) 2018  Bitvis AS

This file is part of KREM.
KREM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

KREM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with KREM. If not, see <http://www.gnu.org/licenses/>.

Bitvis AS
www.bitvis.no
info@bitvis.no

# Change log

For changes please see _\<krem\>/CHANGELOG.txt._
