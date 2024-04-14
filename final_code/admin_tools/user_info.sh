#!/bin/bash

#setting parent path to allow invoke from anywhere
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P )
cd "$parent_path"

#display user info table
sqlite3 ../account_info/database/users.db << EOF

SELECT * FROM users;

EOF
