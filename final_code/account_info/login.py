#!/usr/bin/env python3

import sqlite3
import re
import hashlib
import sys

#start of program
print ("\nWelcome back to Clavis!")
while True:
	ans = input ("\nLog in to Existing Account? (y/n): ")
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

	#possible delete create table for login script?
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

#security question stuff
def questions(username):
	#fetch recorded answers
	cursor.execute("SELECT answer1, answer2, answer3 FROM users WHERE username=?", (username,))
	record = cursor.fetchone()
	#set boolean and counter
	correct = False
	count = 2
	#prompt questions and collect answers
	while not correct:
		#quit to menu prompt
		quit = input("\nContinue to Security Questions? (y/n): ")
		if quit.lower() == "n":
			sys.exit(1)
		elif quit.lower() == "y":
			print("\nQuestion 1: What was the first concert you attended?\n")
			answer1 = input("Question 1 answer: ")
			print("\nQuestion 2: What college did you apply to, but didn't attend?\n")
			answer2 = input("Question 2 answer: ")
			print("\nQuestion 3: What was your childhood nickname?\n")
			answer3 = input("Question 3 answer: ")
			if answer1 != record[0] or answer2 != record[1] or answer3 != record[2]:
				if count == 0:
					input("\nUnable to Login to Account. Press Enter to Continue..")
					sys.exit(1)
				print("\nIncorrect Answer(s). " + str(count) + " more attempt(s)...")
				count -= 1
			else:
				correct = True
		else:
			print("Invalid Input. Try Again")

#login function
def login():
	#initial boolean and counters
	matchLogin = False
	tries = 0
	count = 2
	#username and pass verification
	while not matchLogin:
		username = input("Enter your username: ")
		cursor.execute("SELECT username FROM users WHERE username=?", (username,))
		data = cursor.fetchone()
		#username check
		if data is None:
			tries += 1
			print("Invalid Username. Please try again.")
			#prompt to go back to menu after 3 tries
			while tries > 2:
				capture = input("\nCreate an account instead? (y/n): ")
				print("")
				if capture.lower() == "y":
					sys.exit(1)
				elif capture.lower() == "n":
					break
				else:
					print("Invalid Input. Try Again.")
			#re prompt for username
			continue

		password = input("Enter your password: ")
		cursor.execute("SELECT password FROM users WHERE username=?", (username,))
		data = cursor.fetchone()
		#password check 3 attempts
		while data[0] != hashlib.sha256(password.encode()).hexdigest():
			if count == 0:
				input("Maximum login attempts reached, Press enter to continue...")
				#call security questions
				questions(username)
				break
			print("Invalid Password. " + str(count) + " more attempt(s).")
			password = input("Enter your password: ")
			count -= 1
		#successful login
		matchLogin = True
	#create temp user table to pass to pass manager
	cursor.execute('''DROP TABLE IF EXISTS tempuser''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS tempuser (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT,
			email TEXT,
			password TEXT,
			answer1 TEXT,
			answer2 TEXT,
			answer3 TEXT
			);
			''')
	cursor.execute("SELECT * from users WHERE username=?", (username,))
	user_row = cursor.fetchone()
	cursor.execute("""INSERT INTO tempuser (username, email, password, answer1, answer2, answer3)
			VALUES (?, ?, ?, ?, ?, ?)""",
			(user_row[1], user_row[2], user_row[3], user_row[4], user_row[5], user_row[6],))
	connection.commit()
	input("\nLogin Successful. Press Enter to Continue...\n")


#account login
login()
cursor.close()
connection.commit()
connection.close()
