#!/usr/bin/python

## \file install.py
## \brief KREM Installation file
'''
# Copyright (C) 2018  Bitvis AS
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

# Any modification in this file needs to keep compatibility with Python 2, Python 3, Gitbash and Cygwin.

import os
import fileinput
import io
from contextlib import closing
import subprocess


def print_source_krem():
    print("\nNow source ~/.bashrc or open new terminal to start using KREM.")
    print("Enjoy!\n")


def open_and_write(filename_path, text):
    status = 'FAIL'

    try:
        infile = io.open(filename_path, "r", encoding='utf-8')
        file_data = infile.read()
        infile.close()
        if text in file_data:
            #print(text + " is in .bashrc")
            pass

        else:
            infile = io.open(filename_path, "a+", encoding='utf-8', newline='\n')

            # Keep compatibility between Python 2 and Python 3.
            if type(file_data) == str:
                infile.write("\n" + text)
            else:
                infile.write(("\n" + text).decode('utf-8'))

            #print("Adding to " + env_file + ": " + text)
            infile.close()
        status = 'PASS'

    except Exception as e:
        status = 'FAIL'
        infile.close()
        print("Exception opening a file", e)

    finally:
        return status

def open_and_replace(filename_path, text_search, text_replace):
    status = 'FAIL'
    try:
        with closing(fileinput.FileInput(filename_path, inplace=True, backup='.bak')) as file:
            text_replaced = False
            for line in file:
                if text_search in line:
                    print(text_replace.rstrip())
                    text_replaced = True
                else:
                    print(line.rstrip())

        if text_replaced == True:
            #print(text_search + " replaced by " + text_replace)
            pass
        status = 'PASS'
    except Exception as e:
        status = 'FAIL'
        print("Exception opening a file", e)

    finally:
        return status

def replace_CRLF_LF(file):
    windows_line_ending = '\r\n'
    linux_line_ending = '\n'
    status = 'FAIL'
    try:
        with open(file, 'rb') as f:
            content = f.read()

            # Keep compatibility between Python 2 and Python 3.
            if type(content) == str:
                content = content.replace(windows_line_ending, linux_line_ending)
            else:
                content = content.replace(str.encode(windows_line_ending), str.encode(linux_line_ending))

        with open(file, 'wb') as f:
            f.write(content)

        status = 'PASS'

    except Exception as e:
        status = 'FAIL'
        print("Exception opening a file", e)

    finally:
        return status

if __name__ == '__main__':

    try:
        HOME = os.environ['HOME']
        env_file = HOME + '/.bashrc'
        krem_path = os.path.dirname(os.path.abspath(__file__))
        krempack_path = krem_path + "/krempack"

        # Make paths compatible to GitBash
        uname_o = subprocess.check_output("uname -o", shell=True)
        uname_o = uname_o.rstrip()
        if uname_o == "Msys":
            krem_path = krem_path.replace('\\', '/')
            krem_path = krem_path.replace('C:', '/c')
            krempack_path = krempack_path.replace('\\', '/')
            krempack_path = krempack_path.replace('C:', '/c')

        bashrc_krem_path = "KREM_PATH=" + "\"" + krem_path + "\""
        bashrc_krem_python_path = "KREM_PYTHON_PATH=" + "\"" + krem_path + "\":\"" + krempack_path + "\""
        krem_env2 = "export PATH=$KREM_PATH:$PATH"
        krem_utils_env2 = "export PYTHONPATH=$KREM_PATH" + ":" + "$KREM_PYTHON_PATH" + ":" + "$PYTHONPATH"

        step_1 = open_and_write(env_file, "KREM_PATH=")
        step_2 = open_and_replace(env_file, "KREM_PATH=", bashrc_krem_path)

        step_3 = open_and_write(env_file, "KREM_PYTHON_PATH=")
        step_4 = open_and_replace(env_file, "KREM_PYTHON_PATH=", bashrc_krem_python_path)

        step_5 = open_and_write(env_file, krem_env2)
        step_6 = open_and_write(env_file, krem_utils_env2)

        step_7 = replace_CRLF_LF(env_file)

        if          step_1 == 'PASS'\
                and step_2 == 'PASS'\
                and step_3 == 'PASS'\
                and step_4 == 'PASS'\
                and step_5 == 'PASS'\
                and step_6 == 'PASS'\
                and step_7 == 'PASS':

            print("\nKREM successfully installed.")
            print_source_krem()
        else:
            raise Exception


    except Exception as e:
        print("\n\nKREM was not installed correctly!")
        print("Step 1", step_1)
        print("Step 2", step_2)
        print("Step 3", step_3)
        print("Step 4", step_4)
        print("Step 5", step_5)
        print("Step 6", step_6)
        print("Step 7", step_7)
        print("Please open and issue on https://github.com/Bitvis/krem/issues or contact us.\n")
        print("Exception: ", e)