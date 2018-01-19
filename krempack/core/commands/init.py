
## \file init.py
## \brief Initiates a new KREM project, task or job

'''
# Copyright (C) 2017  Bitvis AS
#
# This file is part of KREM.
#
# KREM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KREM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with KREM.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Bitvis AS 
# www.bitvis.no
# info@bitvis.no
'''

import os
import shutil
import sys

from krempack.common import constants as c
from krempack.common import kremtree


#####################################
#    Generic function to generate files.
#        Call using: generate_file("<path", lambda : func_generator(<params>))
#        func_generator must return string
#######################################
def generate_file(path, func_generator):
    print("Generating file: " + path)

    file = open(path, 'w')
    fileContent = func_generator()

    for line in fileContent:
        file.write(line)

    file.close

    
##################################
#   Copy any file or directory
##################################
def copy_files(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

            
#############################################
#   Generator for global variables file
#       Returns a string of variables
#############################################
def generate_env_main(targetDir, version=None): 
    targetDir = os.path.abspath(targetDir)
    env = []

    if version is not None:
        env.append("VERSION = " + version)

    return env

   

#############################################
#   Deploys the project directory
#############################################
def deploy_template_project(targetDirectory):
    error = None
    templatePath = os.path.join(c.TEMPLATES_PATH, c.TEMPLATE_PROJECT)

    if targetDirectory is not None:
        if not os.path.exists(targetDirectory):
            os.mkdir(targetDirectory)
            print("Creating directory: " + targetDirectory)
    else:    
        targetDirectory = os.getcwd()

    if targetDirectory != None:
        for item in os.listdir(templatePath):

            if os.path.exists(os.path.join(targetDirectory, item)):
                error = True
                print("ERROR: Directory " + item + " exists in target directory.")

        if error != None:
            print("ERROR: Cannot initiate project directory in given location")
        else:
            print("Deploying initial file-structure to " + targetDirectory)
            copy_files(templatePath, targetDirectory)

            env_main_file_path = os.path.join(targetDirectory, c.PROJECT_CONFIG_DIR, c.ENV_FILE_NAME)
            generate_file(env_main_file_path, lambda : generate_env_main(targetDirectory))            
            
            
#################################################
#   Deploys template task
#################################################
def deploy_template_task(taskName):
    templatePath = os.path.join(c.TEMPLATES_PATH, c.TEMPLATE_TASK)
    tasksDir = kremtree.find_common_dir(c.PROJECT_TASKS_DIR)
    
    thisTaskDir = os.path.join(tasksDir, taskName)
    
    
    if os.path.exists(thisTaskDir):
        print('ERROR: Failed to deploy task. Task name already in use.')
    else:
        os.mkdir(thisTaskDir)
        print('Initializing new task')
        copy_files(templatePath, thisTaskDir)
        print('New task located in: ' + os.path.abspath(thisTaskDir))
    

######################################################
#    Deploys template job
######################################################
def deploy_template_job(jobName):
    templatePath = os.path.join(c.TEMPLATES_PATH, c.TEMPLATE_JOB)
    jobsDir = kremtree.find_common_dir(c.PROJECT_JOBS_DIR)
    
    thisJobDir = os.path.join(jobsDir, jobName)
    
    
    if os.path.exists(thisJobDir):
        print('ERROR: Failed to deploy job. Job name already in use.')
    else:
        os.mkdir(thisJobDir)
        print('Initializing new job')
        copy_files(templatePath, thisJobDir)
        print('New job located in: ' + os.path.abspath(thisJobDir))
        
#################################################
#   Calls deploy template functions
#################################################
def deploy_template(template, target=None):

    templatePath = os.path.join(c.TEMPLATES_PATH, template)

    if not os.path.exists(templatePath):
        print("ERROR: template %s not found" % templatePath)
    else:
        if template is c.TEMPLATE_PROJECT:
            deploy_template_project(target)
        elif template is c.TEMPLATE_TASK:
            deploy_template_task(target)
        elif template is c.TEMPLATE_JOB:
            deploy_template_job(target)
            

