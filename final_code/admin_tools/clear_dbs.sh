#!/bin/bash

#setting parent path to allow invoke from anywhere
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P )
cd "$parent_path"

#WILL DELETE ALL USER DATA! PLEASE BE CAREFUL INVOKING THIS
#clear all databases

echo -e "THIS WILL DELETE ALL USER DATA AND DATABASES\n"

read -p "Press Enter to Confirm or Ctrl+C to Stop Script"

rm ../account_info/database/users.db
rm ../program_data/database/*
