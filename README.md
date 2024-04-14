# Linux-Final-Project
A simple password manager created for Intro to Linux Final Project


# The Following Information explains the layout of the program:

# Step 1 user creates an account or logs into active account

- Give user option to select account already made or create new account
- If user has account made already, prompt user to enter set username and password - ( skip to Step 4 if user already has account )
- ( Consider account lockouts for failed login attempts - brute-force prevention )

# Step 1.5 If create account is selected

- Ask for username - twice to confirm selection
- Check for username duplicate ( selected username availability )
- Ask for password - set strong limitations to password while providing instructions
- If password is strong prompt user to enter chosen password once more
- Prompt user "Account activation successful, then prompt user to set security questions in case of 'forgot password'
- Have user answer total of 3 security questions in case of password forgotten.
- Prompt user for 2FA SMS-based code ( Considering we dont have the resources to actually setup 2FA with SMS text messages, we could still add this just to show intentions or complelety remove from plan. )


# Step 2 Account database

Create database realtive to each user that stores their encrypted passwords


# Step 3 Give user exmaple

- Show user random generated word
- Encrypt word and display the encrypted text on screen

# Step 4 User prompt for database entry

- Prompt user the option to retreive set password or create a new one 
- Output error if user selects retrieve with no encrypted password in database


# Step 5 If create new password is selected

- Prompt user to enter the name of the website/application they are creating a password for
- Then prompt the user to enter a plaintext password for said website/application twice ( reccomend strong pass combos - do not require )
- Encrypt set password and form a link/store all 3 inputs together.

# Step 6 If retrieve password is selected
- Clearly communicate "warn" user the consequences of entering the wrong password multiple times ( "Warning: Failure to enter password correctly multiple times will lead to account being locked out until certain conditions are met" )
- Prompt user for name of website/application they are trying to obtain password for
- Check that name entered is exact match to information in database
- If name matches prompt user for plaintext password
- If plaintext password matches echo "Encrypted password has been copied to your clipboard"
- If plaintext doesnt match allow user to retry two more times
- If user enters wrong password total of 3 times they are now locked out of their account and prompted two options ( one if we dont use 2FA )
## Option 1 Display message that an SMS text message has been sent to the phone number entered upon account activation
## Option 2 Allow user to answer all 3 security questions correctly
## Provide brief explanation to user that the account will be locked indefinitely until one of two options is selected and the requirments are met.
