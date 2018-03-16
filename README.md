## Welcome to KREM!

**KREM** is a very lightweight automation framework. **KREM** is also suitable for testing.
**KREM** runs jobs made up of tasks executed in sequence, in parallel or a combination of both.

**KREM** is written in Python, but can execute scripts and programs written in any language.

We are continuously improving **KREM**. We want to keep **KREM** as lightweight and compact as possible, at the same time allowing extended functionality through a plugin interface.

We will provide some plugins, but anyone is more than welcome to contribute.
Plugins can be found here: https://github.com/Bitvis/krem_plugins.git

<font color=green>KREM support Python 2.7 and 3.6 in Linux.</font>
<p><font color=green>KREM in Windows is supported in Git Bash and Cygwin.</font>


Please see the User Manual for more information
<font color=red> docs/KREM_USER_MANUAL.md </font>


--------------------------------------------------------


## Quick start guide

#### get KREM
```
git clone https://github.com/Bitvis/krem.git
```

#### install KREM
```
cd krem directory
./install.py
source ~/.bashrc
```

#### create a project
```
krem init –p project_foo
cd project_foo
```

#### create a job (from template)
```
krem init –j job_foo
```

#### create a task (from template)
```
krem init –t task_foo
```

#### run the job
```
krem run –j job_foo
```

#### list jobs
```
krem list –j
```

#### list tasks
```
krem list –t
```




--------------------------------------------------------


We appreciate any feedback!

Enjoy!



