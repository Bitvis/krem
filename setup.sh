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


#!/bin/bash

env_file=$HOME'/.bashrc'
cd $(dirname "$0") 
krem_path=${PWD}
krempack_path=${PWD}/krempack


cd - >/dev/null

krem_env="export PATH=\"${krem_path}\":"'$PATH'
krem_utils_env="export PYTHONPATH=\"${krem_path}\":\"${krempack_path}\":"'$PYTHONPATH'

echo

check_string=$(grep "$krem_env" "$env_file")
if [[ -z $check_string ]]; then
    echo Adding to ~/.bashrc:  ${krem_env}
    echo $krem_env >> $env_file
else
    echo "PATH is already set"
fi

check_string=$(grep "$krem_utils_env" "$env_file")
if [[ -z $check_string ]]; then
    echo Adding to ~/.bashrc:  ${krem_utils_env}
    echo $krem_utils_env >> $env_file
else
    echo "PYTHONPATH is already set"
fi

echo
echo 'Now source ~/.bashrc or open new terminal to start using KREM.'
echo 'Enjoy!'

echo
