#!/bin/bash

#master script for entire final

#setting parent path to allow invoke from anywhere
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P )
cd "$parent_path"

#clear terminal
clear

#product info/welcome message
cat info.txt

read -p "Press Return to Begin"

#create database directories if they do not exist
mkdir -p ./account_info/database
mkdir -p ./program_data/database

#clear terminal
clear

#run scripts until exit
while [ $? -eq 0 ]
do
	./account_info/account_options.sh
	#ensures infinite loop won't happen on exit
	if [ $? -eq 1 ]
	then
		break
	fi
	python3 ./program_data/password_manager.py
done
