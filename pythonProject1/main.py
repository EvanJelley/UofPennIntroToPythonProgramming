def import_and_create_bank(filename):
    """
    Creates a dictionary of bank account information from a text file.
    Entries should be one per line, in a key:value pair separated by a ':'.
    """

    # Creates an empty bank dictionary
    bank = {}

    # Opens the file in read mode as f
    with open(filename, 'r') as f:

        # Reads the file into a list based on lines
        lines = f.readlines()

        # Iterates over each entry in the bank line
        for line in lines:

            # Strips and separates the line into a list with a comma seperator
            entry = line.strip().split(':')

            # Eliminates blank lines
            if len(entry) <= 1:
                continue

            # Divide each entry into a key and value
            key = entry[0].strip()
            value = entry[1].strip()

            # Tries to cast the value to a float
            try:
                value = float(value)

                bank[key] = bank.get(key, 0) + value

            # Eliminates any key:value pairs that cannot be cast to a float
            except ValueError:
                continue

    return bank


def valid(password):
    """
    Determines if a given password is valid based on the following parameters:
    8 characters long
    1 lowercase
    1 uppercase
    1 number
    """

    # checks length of password. Returns True for passwords >= 8
    if len(password) < 7:
        return False
    # Checks if password has a lowercase letter
    if not any(char.islower() for char in password):
        return False
    # Checks if password has an uppercase letter
    if not any(char.isupper() for char in password):
        return False
    # Checks if password has a digit
    if not any(char.isdigit() for char in password):
        return False
    else:
        return True


def signup(user_accounts, log_in, username, password):
    """
    Checks for validity of username and password.
    Returns False for repeated usernames, username == password, and invalid password
    :param user_accounts: creates a dict with username and password
    :param log_in: creates dict entry with username and False
    :param username: username entry
    :param password: password entry
    :return: Boolean Value
    """

    # Checks for usernames already in the dictionary and returns False if found
    if username in user_accounts:
        print('This username already exists.')
        return False

    # Checks for valid password and ensures password and username are not the same
    if valid(password) and username != password:

        # Creates new user_accounts dict entry with username:password as key:value pair
        user_accounts[username] = password

        # Creates new log_in dict entry with username:False as key:value pair
        log_in[username] = False
        return True
    else:
        print('Your password does not meet the requirements')
        return False


def import_and_create_accounts(filename):
    """
    Imports and reads information from users file and allows user:password pairs to be entered
    in user_accounts dict if they meet requirements of signup() function. Also, cleans data and
    updates login_in dict for any accounts that signup.
    :param filename: txt file with user login info. Should be in 'username - password' pairs
    :return: user_accounts, log_in
    """

    # Define the dictionaries
    user_accounts = {}
    log_in = {}

    # Opens filename in read mode
    with open(filename, 'r') as f:

        # Creates a lines for variable for each line
        lines = f.readlines()

        # Iterates over each line in the file
        for line in lines:

            # Strips and separates the line into a list with a dash seperator
            entry = line.strip().split('-')

            # Eliminates blank lines
            if len(entry) <= 1:
                continue

            # Divide each entry into a key and value
            username = entry[0].strip()
            password = entry[1].strip()

            # Tries to run the signup() function and returns the amended user_accounts and log_in dictionaries
            try:
                signup(user_accounts, log_in, username, password)

            except:
                continue

            return user_accounts, log_in


def login(user_accounts, log_in, username, password):
    """
    Pulls the user_accounts dict and references the username/password combination to ensure they are valid.
    If log in is successful, the log_in Boolean value is changed to True
    :param user_accounts: dictionary with account username and password
    :param log_in: dictionary with log in status
    :param username: attempted username entry
    :param password: attempted password entry
    :return: True, for correctly entered username/password combinations. False, for errors.
    """

    keys = user_accounts.keys()

    for key in keys:
        if key == username:
            attempted_password = user_accounts[key]
            if attempted_password == password:
                log_in[username] = True
                return True
        else:
            continue


def update(bank, log_in, username, amount):
    """
    Function will update the given username/balance in the bank dict with the given amount.
    The given user must be logged in which is checked by confirming True is the value in the log_in dict
    :param bank: dict with username/balance info. Balance will be updated. Cannot go negative.
    :param log_in: dict with username/balance info. Will be used to check log_in status
    :param username: Used to match bank key with log_in key
    :param amount: To be added to existing balance. Cannot cause balance to < 0. Must be numeric.
    :return: True, if account is updated
    """

    # Pulls log_in status and stores it as a variable
    log_in_status = log_in.get(username)

    # Checks if log_in_status is True
    if not log_in_status:
        print('Account is not logged in.')
        return False

    # Continues for logged in accounts
    else:

        # Deals with scenario when username already exists in bank dict
        if username in bank:

            # Returns False if amount will make negative
            if amount + bank.get(username) < 0:
                print("Account balance cannot be negative.")
                return False

            # Returns True and adds amount to current balance in bank dict
            else:
                bank[username] += amount
                return True

        # Handles scenario when username does not yet exist in bank dict
        else:

            # Creates username in bank dict with an amount of 0
            bank[username] = 0

            # Returns False if amount will make negative
            if amount + bank.get(username) < 0:
                print("Account balance cannot be negative.")
                return False

            # Returns True and adds amount to current balance in bank dict
            else:
                bank[username] += amount
                return True

def transfer(bank, log_in, userA, userB, amount):
    """
    The function makes a transfer between two users. UserA is the sender. UserB is the recipient.
    :param bank: The dict that provides the account info in username/balance key/value pairs
    :param log_in: The dict that provides login status in username/Boolean key/value pairs. True is logged in.
    :param userA: The sender. Must be logged. Must have a bank dict entry. Must maintain a positive or zero balance.
    :param userB: The recipient. Can be logged out but must have an entry in log_in. Can be absent from bank.
    :param amount: Amount to be transferred. Will always be positive.
    :return: True if a transfer is completed
    """

    # Pulls log_in status for userA and stores it as a variable
    log_in_status = log_in.get(userA)

    # Checks if log_in_status is True
    if not log_in_status:
        print(userA, 'not logged in.')
        return False

    # Checks for userB entry in log_in dict
    if userB not in log_in:
        print(userB, 'not found')

    # Continues for when userA is logged in
    else:

        # Provides error message for scenario in which userA does not have an entry in bank dict
        if userA not in bank:
            print(userA, "account not found.")
            return False

        # Provides error message for scenario in which userA has insufficient funds
        if bank.get(userA) - amount < 0:
            print(userA, "has insufficient funds.")
            return False

        # For scenarios when userA has a bank entry and sufficient funds
        else:

            # Checks for userB in bank dict
            if userB not in bank:

                # Creates userB in bank dict with an amount of 0
                bank[userB] = 0

            # Subtracts amount from userA account
            bank[userA] -= amount

            # Adds account to userB account
            bank[userB] += amount

            return True

def change_password(user_accounts, log_in, username, old_password, new_password):
    """
    Allows a user to change their password if requirements are met.
    :param user_accounts: Dict log in info in username/password key/value pairs
    :param log_in: Dict with log in status in username/Boolean key/value pairs. True is logged in. Value must be True.
    :param username: Username provided. Must be found in user_accounts dict
    :param old_password: Password provided. Must match current username/password entry in user_accounts.
    :param new_password: New password provided. Will change current entry in user_accounts if requirements are met.
    :return: True if password is changed.
    """

    # Provides error message for scenario when username is not found in user_accounts
    if username not in user_accounts:
        print(username, "not found")
        return False

    # Provides error for when user is not logged in
    if not log_in.get(username):
        print(username, 'not logged in.')
        return False

    # Provides error for an incorrect password
    if old_password != user_accounts.get(username):
        print('Incorrect password')
        return False

    # Provides error for when old password is the same as the new password
    if old_password == new_password:
        print('Password must be different than old password')
        return False

    # Checks if new password is valid
    if not valid(new_password):
        print('Password does not meet requirements')
        return False

    # Changes password if all requirements are met
    else:
        user_accounts[username] = new_password
        return True

def delete_account(user_accounts, log_in, bank, username, password):
    """
    Deletes user from user_accounts, log_in, and bank dict if requirements.
    :param user_accounts: Dict with log_in info.
    :param log_in: Dict with log_in status. Must be True for username key.
    :param bank: Dict with account infor.
    :param username: Provided. Must be in user_accounts.
    :param password: Provided. Must be correct.
    :return: True if account is successfully deleted
    """

    # Provides error message if username is not found in user_accounts
    if username not in user_accounts:
        print(username, 'not found.')
        return False

    # Provides error message if password is incorrect
    if password != user_accounts[username]:
        print('Incorrect password')
        return False

    # Provides error message if user is not logged in
    if not log_in[username]:
        print(username, 'not logged in.')
        return False

    # Deletes entries corresponding to username in user_accounts, log_in, and bank dicts. Returns True
    else:
        del user_accounts[username]
        del log_in[username]
        del bank[username]
        return True

def main():

if __name__ == '__main__':
    main()
