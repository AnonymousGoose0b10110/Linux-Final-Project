#!/usr/bin/env python3

import sqlite3
import re
import hashlib
import sys

#start of program
print ("\nLooking to create a Clavis account? Let's get started!")
while True:
	ans = input ("\nCreate New Account? (y/n): ")
	if ans.lower() == "n":
		sys.exit(1)
	elif ans.lower() == "y":
		print("")
		break
	else:
		print ("Invalid Input. Try Again")
#establish connection to database of all usernames/emails
try:
	connection = sqlite3.connect("./account_info/database/users.db")
	cursor = connection.cursor()

	#create table
	cursor.execute('''CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT,
			email TEXT,
			password TEXT,
			answer1 TEXT,
			answer2 TEXT,
			answer3 TEXT
			);
			''')
	connection.commit()
except sqlite3.Error as e:
	print(f"Error accessing database: {e}")

#username stuff
def username():
	#initial boolean
	newUser = False
	#username entry andverification
	while not newUser:
		username = input("Please enter your desired username: ")
		cursor.execute("SELECT username FROM users WHERE username=?", (username,))
		if cursor.fetchone() is not None:
			while True:
				choice = input("The entered username already exists in our database. Login instead? (y/n): ")
				if choice.lower() == "y":
					sys.exit(1)
				elif choice.lower() == "n":
					break
				else:
					print("Invalid Input. Try Again")
		else:
			print("Username successfully captured.")
			newUser = True
	return username

#email stuff
def email():
	#initial boolean
	newEmail = False
	#email entry and verification
	while not newEmail:
		email = input("\nPlease enter the email you want associated with your Clavis account: ")
		cursor.execute("SELECT email FROM users WHERE email=?", (email,))
		if cursor.fetchone() is not None:
			input("The entered email is already in use. Press enter to try again...")
		else:
			print("Email successfully captured.")
			newEmail = True
	return email

#password stuff
def password():
	#set initial counter
	weakPass = True
	#strength check to ensure strong password
	while weakPass:
		print ("\n--PASSWORD CRITERIA--\n"
		"Must contain the following:\n"
		"8 or more characers\n"
		"1 or more special characters\n"
		"1 or more numbers\n"
		"1 or more uppercase letters\n"
		"1 or more lowercase letters\n"
		"--")
		#user input password
		password = input("Please enter a password that matches all of the above criteria: ")
		#min length check
		if len(password) < 8:
			input("Password must have 8 or more characters. Press enter to try again...")
		#special character check
		elif not re.search(r'[^a-zA-Z0-9s]', password):
			input("Password must contain a special character. Press enter to try again...")
		#number check
		elif not re.search(r'[0-9]', password):
			input("Password must have 1 or more numbers. Press enter to try again...")
		#uppercase check
		elif not re.search(r'[A-Z]', password):
			input("Password must have 1 or more uppercase letters. Press Enter to Try again...")
		#lowercase check
		elif not re.search(r'[a-z]', password):
			input("Password must have 1 or more lowercase letters. Press Enter to try again...")
		#successful password creation
		else:
			print("Password successfully captured.")
			weakPass = False
	return hashlib.sha256(password.encode()).hexdigest()

#security question stuff
def security():
	#establish security questions
	print("\nNow that we've got you set up, let's add some security questions to secure your account.")
	#prompt questions and collect answers
	print("\nQuestion 1: What was the first concert you attended?\n")
	answer1 = input("Question 1 answer: ")
	print("\nQuestion 2: What college did you apply to, but didn't attend?\n")
	answer2 = input("Question 2 answer: ")
	print("\nQuestion 3: What was your childhood nickname?\n")
	answer3 = input("Question 3 answer: ")
	return (answer1, answer2, answer3)

#functions grouped
def account_creation():
	user = username()
	mail = email()
	passwd = password()
	answr = security()
	cursor.execute("INSERT INTO users (username, email, password, answer1, answer2, answer3) VALUES (?, ?, ?, ?, ?, ?)",
			(user, mail, passwd, answr[0], answr[1], answr[2]))
	input("\nAccount Successfully Created. Press Enter and Select Login...")

account_creation()
cursor.close()
connection.commit()
connection.close()
sys.exit(1)
