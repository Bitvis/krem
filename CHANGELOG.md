# KREM Changelog


-----------------------------------------

### v2.1.1
----------

Released: 2018-03-02

* **bugfix:** running a job based on job number did not always result in running the requested job


### v2.1.0
----------

Released: 2018-03-02

* **bugfix:** _full\_run\_nr_ added to task object passed to task functions
* **bugfix:** Sort assigned numbers to output from _krem list_
* **bugfix:** Allow spaces in paths in setup.py
* Extended types of arguments that can be passed from job to task
* MANUAL ported to markdown format
* CHANGELOG ported to markdown format
* Renamed plugin _entrypoints_ to plugin _hooks_
* Added hook _job\_progress\_text_
* Added support for running KREM in Git Bash in Windows
* Added support for running KREM in Cygwin



### v2.0.0
----------

Released: 2018-02-14

- renamed task function 'variables' to 'arguments'


### v1.4.0
----------

Released: 2018-02-13

##### See also porting instructions below for more info

* bugfix: task object and not task name is now passed to pre_task_execution plugin entry-point
* renamed <krem project>/output/<job>/latest/results.txt to <krem project>/output/<job>/latest/results
* renamed <krem project>/output/<job>/latest/run.txt to <krem project>/output/<job>/latest/execution.log
* renamed <krem project>/output/info.txt to <krem project>/output/<job>/latest/info
* renamed <krem project>/tasks/<task>/setup.txt <krem project>/tasks/<task>/task.cfg
* renamed <krem project>/tasks/<task>/run.py <krem project>/tasks/<task>/task.py
* added <krem project>/library/colorconstants.py with color contants to be used in jobs, tasks and plugins
* changed logging level in job template from debug to info
* replaced function job.get_job_result() with function job.get_task_results().

##### Porting from v1.3.x to v1.4.0

* modify <krem project>/jobs/<job>/job.py:

  from:

  ```python
  path, job_name = os.path.split(os.path.dirname(__file__))
  job = krem.Job(job_name, rc)
  ```

  to:

  ```python
  job = krem.Job(__file__, rc)
  ```

* add 'task' argument as the first argument in all task functions
* rename <krem project>/tasks/<task>/run.py to <krem project>/tasks/<task>/task.py
* rename <krem project>/tasks/<task>/setup.txt to <krem project>/tasks/<task>/task.cfg
* modify <krem project>/tasks/<task>/task.cfg: from 'TASK_FILE = run.py' to 'TASK_FILE = task.py'
* copy <krem installation>/krempack/templates/project/library/task.py to <krem project>/library/task.py
* copy <krem installation>/krempack/templates/project/library/colorcodes.py to <krem project>/library/colorcodes.py
* copy <krem installation>/krempack/templates/project/library/returncodes.py to <krem project>/library/returncodes.py
* function job.get_job_result() is removed and replaced with function job.get_task_results().
  Note that job.get_job_result() resturned a single return code while job.get_task_results() return a list of all task results


### v1.3.3

----------

Released: 2018-01-31

- **bugfix:** task object and not task name is now passed to pre_task_execution plugin entry-point


### v1.3.2

----------

Released: 2018-01-26

* krem no longer hang when running several parallel tasks


### v1.3.1

----------

Released: 2018-01-23

* template task and job can be run without modifications
* updated MANUAL


### v1.3.0

----------

Released: 2018-01-19

* renamed plugin entry points

	`pre_task_execution` -> `pre_task_function_call`

	`post_task_execution` -> `post_task_function_call`

	`job_configuration` -> `job_start`

	`job_post_processing` -> `job_end`

	`pre_task_setup` -> `pre_task_execution`

	`task_post_processing` -> `post_task_execution`

### v1.2.1

------

Released: 2018-01-19

* added library/plugins
* updated MANUAL


### v1.2.0

----------

Released: 2018-01-10

* Added setup.py to library directory in project template with default function for plugin setup.
* Added call to plugin setup in job template

### v1.1.0

----------

Released: 2018-01-08

* Added plugin entrypoints "pre_task_setup" and "task_post_processing"
* **bug fix:** Task results set before plugin entrypoint "post_task_execution"

### v1.0.0

----------

Released: 2018-08-01

- Initial release
