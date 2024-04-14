#!/usr/bin/env python3
import os
import sqlite3
import hashlib
import secrets
import string
import subprocess
import time

# Functions to create colored text
def green_message(message, color_code=32):
    formatted_green_message = f"\033[{color_code};1m{message}\033[0m"
    print(formatted_green_message)
    return ""

def red_message(message, color_code=31):
    formatted_red_message = f"\033[{color_code};1m{message}\033[0m"
    print(formatted_red_message)

def blue_message(message, color_code=34):
    formatted_blue_message = f"\033[{color_code};1m{message}\033[0m"
    print(formatted_blue_message)

# Function to create or connect to user-specific database
def create_or_connect_user_db(username):
    db_filename = f"./program_data/database/{username}_passwords.db"

    try:
        connection = sqlite3.connect(db_filename)
        cursor = connection.cursor()

        # Create a table to store website/application names and encrypted passwords
        cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           website TEXT NOT NULL,
                           account_password TEXT NOT NULL);''')

        connection.commit()
        green_message(f"Connected to {username}'s database")

    except sqlite3.Error as e:
        red_message(f"Error creating or connecting to database: {e}")

    finally:
        if connection:
            connection.close()

# Function to encrypt the password using SHA-256
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to generate a random password
def generate_random_password():
    min_length = 12  # You can adjust the length of the password as needed
    max_length = 24
    password_length = secrets.randbelow(max_length - min_length + 1) + min_length

    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(password_length))

# Function to store a new password for a website/application
def store_password(username, website):
    db_filename = f"./program_data/database/{username}_passwords.db"


    connection = None

    try:
        connection = sqlite3.connect(db_filename)
        cursor = connection.cursor()

        # Check if the website/application name is already in use
        cursor.execute("SELECT website FROM passwords WHERE website=?", (website,))
        result = cursor.fetchone()

        if result:
            red_message(f"The website/application name '{website}' is already in use.")
            red_message("Please choose a different website/application name.")
            return

        # Generate a random password for encryption
        random_password = generate_random_password()

        # Encrypt the password
        encrypted_password = encrypt_password(random_password)

        # Insert the website and encrypted password into the table
        cursor.execute("INSERT INTO passwords (website, account_password) VALUES (?, ?)",
                       (website, encrypted_password))

        connection.commit()
        green_message(f"Password successfully stored for {website}")  # Display the generated password

    except sqlite3.Error as e:
        red_message(f"Error storing password: {e}")

    finally:
        if connection:
            connection.close()

# Function to retrieve a password for a website/application
def retrieve_password(username, website):
    db_filename = f"./program_data/database/{username}_passwords.db"


    try:
        connection = sqlite3.connect(db_filename)
        cursor = connection.cursor()

        # Retrieve the encrypted password for the website
        cursor.execute("SELECT account_password FROM passwords WHERE website=?", (website,))
        result = cursor.fetchone()

        if result:
            encrypted_password = result[0]
            #display password in terminal
            print("Encrypted Password:", encrypted_password)
            return encrypted_password
        else:
            red_message(f"Password not found for {website}.")
            return None

    except sqlite3.Error as e:
        red_message(f"Error retrieving password: {e}")
        return None

    finally:
        if connection:
            connection.close()
# Function to display list of website/application names for the user using AWK
def display_website_list(username):
    db_filename = f"./program_data/database/{username}_passwords.db"


    try:
        # Execute the AWK script using subprocess to display the list
        subprocess.run(["awk", "-f", "./program_data/display_website_list.awk", db_filename])

    except FileNotFoundError:
        red_message("AWK not found. Please make sure AWK is installed and accessible on the system.")

#display function to perl/html
def display_all(username):
    db_filename = f"./program_data/database/{username}_passwords.db"


    try:
        connection = sqlite3.connect(db_filename)
        cursor = connection.cursor()

        # Retrieve all info
        cursor.execute("SELECT DISTINCT website FROM passwords")
        website = cursor.fetchall()

        if website:
            cursor.execute("SELECT DISTINCT account_password FROM passwords")
            encrypted_passwords = cursor.fetchall()
            webStr = ""
            passStr = ""
            #convert tuples to strings
            for item in website:
                webStr = webStr + str(item)
            for item in encrypted_passwords:
                passStr = passStr + str(item)
            #trim leftover tuple elements
            webStr = webStr.translate({ord("("): None})
            webStr = webStr.translate({ord(")"): None})
            webStr = webStr.translate({ord("'"): None})
            passStr = passStr.translate({ord("("): None})
            passStr = passStr.translate({ord(")"): None})
            passStr = passStr.translate({ord("'"): None})
            #pass strings as args to perl script
            subprocess.run([ "perl", "./program_data/web_and_pass.pl", webStr, passStr])
            os.system('rm program_data/web_and_pass.html')
        else:
            red_message(f"Nothing to Display.")
            return None

    except sqlite3.Error as e:
        red_message(f"Error retrieving info: {e}")
        return None

    finally:
        if connection:
            connection.close()


# User Interactive Menu
if __name__ == "__main__":
    db_filename = "./account_info/database/users.db"
    connection = None


    try:
        connection = sqlite3.connect(db_filename)
        cursor = connection.cursor()

        # Create OR connect to the user-specific password database
        cursor.execute("SELECT * FROM tempuser")
        grab = cursor.fetchone()
        username = grab[1]
        cursor.execute("DROP TABLE IF EXISTS tempuser")   #table no longer need, repeat of login script,
        create_or_connect_user_db(username)			#but more secure delete here
        # User interaction loop
        while True:
            subprocess.run(["/usr/bin/python3", "./program_data/clavis_banner.py"]) # Call upon Banner script
            green_message("Choose an option:")
            blue_message("1. Store a new password")
            blue_message("2. Retrieve a password")
            blue_message("3. Display a list of stored website/application names")
            blue_message("4. Display a list of stored websites with respective passwords")
            blue_message("5. Exit")
            choice = input(green_message("Enter your choice (1/2/3/4/5): "))
            if choice == "1":
                website = input(green_message("Enter the website/application name: "))
                store_password(username, website)
                input("Password for " + website + " successfully stored. Press Enter to Continue...")
                os.system('clear')
            elif choice == "2":
                website = input(green_message("Enter the website/application name: "))
                retrieve_password(username, website)
                input("Press Enter to Continue...")
                os.system('clear')
            elif choice == "3":
                display_website_list(username)
                input("Press Enter to Continue...")
                os.system('clear')
            elif choice == "4":
                display_all(username)
                os.system('clear')
            elif choice == "5":
                green_message("Exiting...")
                time.sleep(.5)
                break
            else:
                red_message("Invalid choice. Please try again.")
                input("Press Enter to Continue...")
                os.system('clear')

    except sqlite3.Error as e:
        red_message(f"Error checking account password: {e}")

    finally:
        if connection:
            connection.close()

