## Welcome to KREM!

**KREM** is a very lightweight automation framework. **KREM** is also suitable for testing.
**KREM** runs jobs made up of tasks executed in sequence, in parallel or a combination of both.

**KREM** is written in Python, but can execute scripts and programs written in any language.

We are continuously improving **KREM**. We want to keep **KREM** lightweight and compact as possible, but allow to extend functionality through a plugin interface.

We will provide some plugins, but anyone is more than welcome to contribute.
Plugins can be found here: https://github.com/Bitvis/krem_plugins.git


##### Support python 2.7 and 3.6

--------------------------------------------------------


## Quick start guide
(Please see the MANUAL for more information and a simple tutorial)

#### get KREM
```
git clone https://github.com/Bitvis/krem.git
```

#### install KREM
```
cd krem directory
./setup.sh
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



