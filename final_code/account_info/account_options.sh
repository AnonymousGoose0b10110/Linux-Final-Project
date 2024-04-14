#!/bin/bash

#account selection; login or create an account

#select menu to create or login to account
while true; do
	clear
	echo  "-Clavis Encryption-"
	PS3="Please select an account option: "
	select option in Login Create Quit
	do
    	case $option in
		#call login function
		Login)
	    		./account_info/login.py
	    		if [ $? -eq 1 ]
	    		then
	    			break
	    		fi
			clear
			break 2
	    		;;
		#call create function
		Create)
	    		./account_info/create.py
			if [ $? -eq 1 ]
			then
				break
			fi
			clear
			break 2
	    		;;
		#terminate
		Quit)
            		echo "-Program Terminated-"
            		exit 1
            		;;
		*)
	    		read -p "Invalid Option: $REPLY. Press Enter to Try Again..."
			break
	    		;;
        	esac
	done
done
