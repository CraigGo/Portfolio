import csv
import os
from copy import copy   # don't remove need for Test Cases
from cryptography.fernet import Fernet

secret_file = "cellar_secrets.txt"
customer_file = "cellar_cust.csv"
wine_cellar_file = "cellar.csv"


class App:
    """Main class that loads data from the customer csv file and from
    the cellar csv file.  Set active_account to None, until a valid
    user logs in.
    """
    def __init__(self):
        self.accounts = {}
        self.active_account = None
        self.load_accounts()

    def load_accounts(self):
        """ loads customer csv file and cellar csv file into memory

        TODO:  need to add file load error handling
        """
        with open(customer_file, 'rt', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                email = row[2].lower()
                self.accounts[email] = Cellar()

        with open(wine_cellar_file, 'rt', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                email = row[0].lower()
                bottle = Bottle(*row[1:17])
                self.accounts[email].add_bottles(bottle)

    def login(self, inp_email, text_pwd):
        """login function takes the email and password strings and
        verifies the information against the customer csv file.

        Args:
            inp_email (str): user inputed email name.
            text_pwd (str): user inputed password.

        Returns:
            bool: The return value, True for success, False otherwise.
        """
        inp_email = inp_email.lower()
        with open(customer_file, 'rt', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                byte_str = str(self.decryptor(row[3]))
                if inp_email.lower() == row[2].lower() and byte_str[2:-1] == text_pwd:
                    self.active_account = inp_email.lower()
                    return True
        return False

    def logout(self):
        """logout function saves the cellar memory to a CSV file on disk.
        and then sets the active_account to None.
        """
        self.save_accounts()
        self.active_account = None

    def save_accounts(self):
        """save_accounts function is called by logout to save what's in
        memory to the cellar CSV file on disk.
        """
        with open(wine_cellar_file, 'wt', newline='') as f:
            headers = ["email","color","category","size","value","quantity","vintage",
                        "wine","country","locale","producer","varietal","beginConsume",
                        "endConsume","rating","row","col"]
            writer = csv.DictWriter(f, headers)
            data = [dict(vars(wine),**{"email": email}) for email, cellar in self.accounts.items() for key, wine in cellar.bottles.items()]
            writer.writeheader()
            writer.writerows(data)

    def add_account(self, fname, lname, inp_email, text_pwd, max_row, max_col):
        """Takes account information and appends it to the existing
        customer csv file.

        Args:
            fname (str): first name.
            lanme (str): last name.
            inp_email (str): email.
            text_pwd (str): password in plain text.
            max_row (str): maximum number of rows in cellar.
            max_col (str): maximum number of columns in cellar.
        Returns:
            bool: The return value, True for success, False otherwise.
        """
        inp_email = inp_email.lower()
        if inp_email not in self.accounts.keys():
            encrypted_pwd = str(self.encryptor(text_pwd))
            new_row = (
                fname + "," + lname + "," + inp_email + "," +
                # Removed b' at the beginning and ' at end of string
                encrypted_pwd[2:-1] + "," + str(max_row) + "," +
                str(max_col) + "\n"
            )
            with open(customer_file, 'at', newline='') as s:
                s.write(new_row)
            self.accounts[inp_email] = Cellar()
            return True
        return False

    def remove_account(self, inp_email, text_pwd):
        """Removes an account in the existing customer csv file.

        Args:
            fname (str): first name.
            lanme (str): last name.
            inp_email (str): email.
            text_pwd (str): password in plain text.
            max_row (str): maximum number of rows in cellar.
            max_col (str): maximum number of columns in cellar.
        Returns:
            bool: The return value, True for success, False otherwise.
        """
        temp_file = "~temp_wine_cust.tmp"
        account_removed = False
        inp_email = inp_email.lower()
        header = ["fname", "lname", "email", "pwd", "cellar_rows", "cellar_cols"]
        with open(customer_file, 'rt', newline='') as f, open(temp_file, 'wt', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                byte_str = str(self.decryptor(row[3]))
                if inp_email.lower() == row[2].lower() and byte_str[2:-1] == text_pwd:
                    account_removed = True
                    continue
                else:
                    writer.writerow(row)
        os.remove(customer_file)
        os.rename(temp_file, customer_file)
        return account_removed

    def encryptor(self, text_pwd):
        """Encrypts a string using a secret token that contains the key
        to encrypt/decrypt.

        Args:
            text_pwd: is the text to be encrypted.

        Returns:
            Returns the encrypted text.
        """
        with open(secret_file, 'rt', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            key = next(reader, None)[0]
            f = Fernet(key)
            cipher_text = f.encrypt(bytes(text_pwd, encoding='utf8'))
        return cipher_text

    def decryptor(self, cipher_text):
        """Decrypts a string using a secret token that contains the key
        to encrypt/decrypt.

        Args:
            cypher_text: is the encrypted string to be decrypted.

        Returns:
            Returns plain text.
        """
        with open(secret_file, 'rt', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            key = next(reader, None)[0]
            cipher_suite = Fernet(key)
            plain_text = cipher_suite.decrypt(bytes(cipher_text, encoding='utf8'))
        return plain_text

    def secrets(self):
        """Secrets generates the secret token. The secret token is
        stored in the secrets.txt file and only needs to be used once as
        shows below:

        fernet_key = fernet.Fernet.generate_key()
        """
        pass

class Cellar:
    """The Cellar Class can add/remove bottles as well as increment or
    decrement the bottle count.  The Class can also select specific bottles
    and can display the bottles in the cellar.
    """

    def __init__(self):
        self.bottles = {}

    def add_bottles(self, bottle):
        """adds bottles to the cellar. If the bottle already exists, then
        the quantity is incremented.

        Args:
            bottle: contains all the attributes of a bottle.

        TODO:  Need to check for if the bottle already exists in that
        specific location.
        """
        key = (bottle.wine, bottle.vintage, bottle.size)

        if key not in self.bottles:
            self.bottles[key] = bottle
        else:
            self.bottles[key].quantity += bottle.quantity

    def remove_bottles(self, bottle):
        """removes bottles in the cellar. If the quantity to decrement
        is > than current, then decremenet quantity. Else, if last bottle
        the bottle will be removed.

        TODO: Add error msg when quantity > what is in cellar.  It silently
        fails today, with no error msg.

        Args:
            bottle instance.

        """
        key = (bottle.wine, bottle.vintage, bottle.size)

        if key in self.bottles:
            if bottle.quantity <= self.bottles[key].quantity:
                self.bottles[key].quantity -= bottle.quantity
            if self.bottles[key].quantity < 1:
                del self.bottles[key]

    def select_bottles(self, index):
        """Selects the bottle based on index value

        Args:
            index: contains the index number.

        Returns:
            Returns the list of the bottle details for that index.
        """
        return list(self.bottles.values())[index]

    def __repr__(self):
        """Returns a list of the bottles. """
        value = "".join([f"\t({index + 1})\t{bottle.quantity}\t{bottle.vintage}\t{bottle.wine}\n" for index, bottle in enumerate(self.bottles.values())])
        return value


class Bottle:
    """Bottle Class that contains all the details of the bottle and will
    return a list of the bottle details."""
    def __init__(self, color, category, size, value,
        quantity, vintage, wine, country, locale, producer,
        varietal, beginConsume, endConsume, rating, row, col):
        self.color = color
        self.category = category
        self.size = size
        self.value = float(value.strip(' $'))
        self.quantity = int(quantity)
        self.vintage = int(vintage)
        self.wine = wine
        self.country = country
        self.locale = locale
        self.producer = producer
        self.varietal = varietal
        self.beginConsume = int(beginConsume)
        self.endConsume = int(endConsume)
        self.rating = rating
        self.row = int(row)
        self.col = int(col)

    def __repr__(self):
        value = (
            f"{'-' * 60}\n"
            f"{self.wine:^50}\n"
            f"{'-' * 60}\n"
            f"Quantity: {self.quantity}\n"
            f"Wine name: {self.wine}\n"
            f"Size: {self.size}\n"
            f"Color: {self.color}\n"
            f"Category: {self.category}\n"
            f"Vintage: {self.vintage}\n"
            f"Value: ${self.value:.2f}\n"
            f"Locale: {self.locale:<10}\n"
            f"Country: {self.country:<10}\n"
            f"Producer: {self.producer:<10}\n"
            f"Varietal: {self.varietal:<10}\n"
            f"Drink after: {self.beginConsume:<10}\n"
            f"Drink by: {self.endConsume:<10}\n"
            f"Rating: {self.rating:.2}\n"
            f"Location (row,col): ({self.row + 1}, {self.col + 1})\n"
        )
        return value


# ################## Engine Test Cases ################################
# Below are all the test cases for the Engine that verifies that the
# Engine is working.
#######################################################################

# app = App()

# #######  Login
# print("\n*** Tests: Login")
# print("*" * 60)
# print("Login Status:", app.login("craigfl@hotmail.com", "Craig101"))
# print("Logged In:", app.active_account, app.active_account == "craigfl@hotmail.com")

# #######  Add / Remove Accounts
# print("\n*** Tests: Add / Remove Accounts")
# print("*" * 60)
# print("Account Add:", app.add_account("Bill", "Salt", "Bill@aws.com", "password999", "20", "5"))
# print("Account Add:", app.add_account("Sally", "Zimmer", "Sally@yahoo.com", "password123", "15", "20"))
# print("Account Add:", app.add_account("Tim", "Goodman", "Good@aol.com", "password456", "10", "30"))
# print("Account Remove:", app.remove_account("Sally@yahoo.com", "password123"))
# print("Account Remove:", app.remove_account("Bill@aws.com", "password999"))
# print("Account Remove:", app.remove_account("Good@aol.com", "password456"))

# #######  Test cases
# print("\n*** Tests: Retrieve Wine & displays bottle #3")
# print("*" * 60)
# print(app.accounts[app.active_account])     # prints out the wine for the logged in user
# print(app.accounts[app.active_account].select_bottles(2))  # Display wine #3

# #######  Add / Remove Bottles
# print("\n*** Tests: Select bottle #9 and removes 1 bottle")
# print("*" * 60)
# print(app.accounts[app.active_account].select_bottles(8))   # select bottle #9
# stags = copy(app.accounts[app.active_account].select_bottles(8))     # Copy #9 to change quantity
# stags.quantity = 1  #decrement by 1
# app.accounts[app.active_account].remove_bottles(stags)   # remove a bottle

# #######  Adding a Bottle
# print("\n*** Tests: Add a new Bottle - Blahford and increment the count by 4")
# print("*" * 60)
# beauford = Bottle("Red", "Dry", "750ml", "12.52", "4", "2007", "Blahford", "USA", "foo", "bar", "Zin", "1776", "2044", "92", "1", "1")
# app.accounts[app.active_account].add_bottles(beauford)      # Add a Bottle
# print(app.accounts[app.active_account])     # prints the wine for the logged in user
# app.accounts[app.active_account].add_bottles(beauford)      # Add another Bottle, increments quantity by 4
# print(app.accounts[app.active_account])     # prints out the wine for the logged in user
