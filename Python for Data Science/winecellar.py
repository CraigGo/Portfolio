import csv
import os
import getpass
from copy import copy
from datetime import datetime
from wineengine import App, Cellar, Bottle

customer_file = "cellar_cust.csv"
debug = False


class Menu:
    """Main Menu class - All menus/UI are located in this class"""

    def clear_screen(self):
        """Clears the screen for multiple operating systems """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n")

    def main_menu(self):
        """Main menu function and is the first screen the customer will see."""
        while True:
            if not(debug):
                appMenu.clear_screen()
            value = (
                f"Welcome to the Wine Cellar\n"
                f"{'-' * 60}\n"
                f"(1) Login\n"
                f"(2) Create an account\n"
                f"(3) Remove your account\n"
                f"(4) Logout\n"
            )
            print(value)

            cmd = input("What would you like to do?  ")
            if cmd in "1234":
                break
            else:
                print(f"\nInvalid entry. Please select 1-4.\n")
                input(f"Press [ENTER] to continue\n")

        if cmd == "1":
            appMenu.login_menu()
        elif cmd == "2":
            appMenu.account_creation_menu()
        elif cmd == "3":
            appMenu.account_deletion_menu()
        else:
            appMenu.logout_menu()

    def login_menu(self):
        """Login menu that presents the UI for the login function. Function
        getpass is called to not echo the typed letters on the screen. If
        Login function returns True, then proceed to Cellar Mgmt menu, else
        return to the main_menu.
        """
        login_valid = False

        while True:
            if not(debug):
                appMenu.clear_screen()

            print(f"Login")
            print(f"{'-' * 60}\n")
            print(f"Enter the following information:\n")
            email = str(input(f"E-mail name: "))
            typed_pwd = getpass.getpass(f"Password: ")

            if app.login(email, typed_pwd):
                login_valid = True
                break
            else:
                print(f"\nError: Email or Password was incorrect.\n")
                ans = input(f"Press [ENTER] to retry or [M] for Main Menu. ")
                if ans.upper() == "M":
                    login_valid = False
                    break

        if login_valid:
            appMenu.cellar_mgmt_menu()
        else:
            appMenu.main_menu()

    def logout_menu(self):
        """Logout menu is selected, calls logout function, where cellar results
        in memory are written out to file.
        """
        app.logout()
        print(f"\nThank you for using the Wine Cellar.\n")

    def account_creation_menu(self):
        """Account creation menu, if email or password are correct, then account
        was created successfully, else a False is returned.
        """
        if not(debug):
            appMenu.clear_screen()

        print(f"Create a new account")
        print(f"{'-' * 60}")
        print(f"Enter the following information:\n")
        fname = str(input(f"First name: "))
        lname = str(input(f"Last name: "))
        max_rows = str(input(f"# of rows in your cellar: "))
        max_cols = str(input(f"# of columns in your cellar: "))
        email = str(input(f"E-mail name: "))
        # call getpass to remove password echo
        typed_pwd = getpass.getpass(f"Password: ")

        if (app.add_account(fname, lname, email, typed_pwd, max_rows, max_cols)):
            print(f"\nSuccess!  The account was created.\n")
            input(f"Press [ENTER] to return to the Main Menu.")
        else:
            print(f"\nError:  Account already exists.")
            input(f"Press [ENTER] to return to Main Menu.")

        appMenu.main_menu()

    def account_deletion_menu(self):
        """Account deletion menu, if email or password are correct, then account
        is removed, else a False is returned.
        """
        if not(debug):
            appMenu.clear_screen()

        print(f"Delete an account")
        print(f"{'-' * 60}\n")
        print(f"Enter the following information:\n")
        email = str(input(f"E-mail name: "))
        typed_pwd = getpass.getpass(f"Password: ")

        if app.remove_account(email, typed_pwd):
            print(f"\nSuccess!  The account was removed.\n")
            input(f"Press [ENTER] to return to the Main Menu.")
        else:
            print(f"\nError:  e-mail or password was incorrect.")
            input(f"Press [ENTER] to return to Main Menu.")

        appMenu.main_menu()

    def cellar_mgmt_menu(self):
        """Cellar mgmt main menu, only get here after a valid login."""
        while True:
            if not(debug):
                appMenu.clear_screen()
            value = (
                f"Cellar Management\n"
                f"{'-' * 60}\n"
                f"(1) Add a bottle\n"
                f"(2) Drink/Remove a bottle\n"
                f"(3) Reports\n"
                f"(4) Return to Main Menu\n"
            )
            print(value)

            cmd = input(f"What would you like to do?  ")
            if cmd in "1234":
                break
            else:
                print(f"\nInvalid entry. Please select 1-4.\n")
                input(f"Press [ENTER] to continue\n")

        if cmd == "1":
            appMenu.add_bottle_menu()
        elif cmd == "2":
            appMenu.drink_remove_bottle_menu()
        elif cmd == "3":
            appMenu.reports_menu()
        else:
            appMenu.main_menu()

    def add_bottle_menu(self):
        """Add Bottle menu provies 2 choices: (1) add a brand new bottle or
        (2) increase the quantity of an existing wine.

        TODO: Add cellar row & column checking
        """
        while True:
            if not(debug):
                appMenu.clear_screen()
            print(f"Add a Bottle")
            print(f"{'-' * 60}")
            print(f"(1) Add a new bottle to the cellar")
            print(f"(2) Increase the quantity of an existing wine\n")
            print(f"What would you like to do?\n")
            cmd = input(f"press [M] to return to Cellar Management: ")
            if cmd.upper() == "M":
                break
            elif cmd == "1":
                if not(debug):
                    appMenu.clear_screen()
                print(f"Add a Bottle")
                print(f"{'-' * 60}")
                print(f"Enter the following information:\n")
                values = []
                values.append(input(f"Color (red/white): "))
                values.append(input(f"Category (dry/sweet): "))
                values.append(input(f"Size 750ml/1.5l: "))
                values.append(input(f"Value ($): "))
                values.append(input(f"Quantity: "))
                values.append(input(f"Vintage (year): "))
                bottle_name = input(f"Wine name: ")
                values.append(bottle_name)
                values.append(input(f"Country: "))
                values.append(input(f"Locale: "))
                values.append(input(f"Producer: "))
                values.append(input(f"Varietal (Pinot/Cabernet): "))
                values.append(input(f"Begin Consuming Year: "))
                values.append(input(f"End Consuming Year: "))
                values.append(input(f"Rating: "))
                row_name = input(f"Cellar Row: ")
                values.append(str(int(row_name) - 1))
                col_name = input(f"Cellar Column: ")
                values.append(str(int(col_name) - 1))
                bottle_details = Bottle(*values)
                print("\nAdding Bottle: ", bottle_name, end='', flush=False)
                app.accounts[app.active_account].add_bottles(bottle_details)
                input(f"...   Success!  \n\nPress [Enter] to continue")

            elif cmd == "2":
                if not(debug):
                    appMenu.clear_screen()

                print(f"Add a Bottle")
                print(f"{'-' * 60}")
                print(app.accounts[app.active_account])
                print(f"{'-' * 60}")

                bottle_no = int(input(f"Enter the Bottle #: "))
                quant_inc = int(input(f"Enter the amount to increase: "))
                if bottle_no in range(1, len(app.accounts[app.active_account].bottles) + 1):
                    original_bottle = app.accounts[app.active_account].select_bottles(bottle_no - 1)
                    bottle_details_copy = copy(original_bottle)
                    bottle_details_copy.quantity = quant_inc
                    app.accounts[app.active_account].add_bottles(bottle_details_copy)
                    print(f"\nUpdating quantity for: {bottle_details_copy.wine} by {quant_inc}...   ", end='', flush=False)
                    input(f"Success!  \n\nPress [Enter] to continue")
                else:
                    input(f"\nError: Invalid entry. Press [Enter] to continue")
            else:
                input(f"\nInvalid entry. Press [Enter] to continue")

        appMenu.cellar_mgmt_menu()

    def drink_remove_bottle_menu(self):
        """Menu to remove a quantity of wine from an existing list. Must create a
        shallow copy of of bottle selected.
        """
        while True:
            if not(debug):
                appMenu.clear_screen()

            print(f"Remove a Bottle")
            print(f"{'-' * 68}")
            print(f"\t #\tQty\tYear\tWine Name")
            print(app.accounts[app.active_account])
            print(f"{'-' * 68}")
            print(f"Enter the Bottle # to remove from inventory or")
            try:
                cmd = input(f"press [M] to return to the Cellar Management menu: ")
                if cmd.upper() == "M":
                    break
                elif cmd.isdigit:
                    quant_inc = input(f"\nEnter the amount to decrease: ")
                    if quant_inc.isdigit:
                        quant_inc = int(quant_inc)
                        bottle_no = int(cmd)
                        if bottle_no in range(1, len(app.accounts[app.active_account].bottles) + 1):
                            original_bottle = app.accounts[app.active_account].select_bottles(bottle_no - 1)
                            bottle_details_copy = copy(original_bottle)
                            bottle_details_copy.quantity = quant_inc
                            app.accounts[app.active_account].remove_bottles(bottle_details_copy)
                            print(f"\nUpdating quantity for: {bottle_details_copy.wine} by {quant_inc}...   ", end='', flush=False)
                            input(f"Success!  \n\nPress [Enter] to continue")
                        else:
                            input(f"\nError: Invalid entry. Press [Enter] to continue")
                    else:
                        input(f"\nError: Invalid entry. Press [Enter] to continue")
            except:
                input(f"\nError: Invalid entry. Press [Enter] to continue")

        appMenu.cellar_mgmt_menu()

    def reports_menu(self):
        """Reports menu that offers 6 different reports.

        TODO: move customer_file load to engine file to store the max_rows and
        max_cols to be used here.  Then remove the import csv.
        """
        currentYear = int(datetime.now().year)
        while True:
            if not(debug):
                appMenu.clear_screen()
            print(f"Wine Cellar Reports")
            print(f"{'-' * 60}")
            print(f"(1) Wine List")
            print(f"(2) Wine Detail Cards")
            print(f"(3) Cellar Grid View")
            print(f"(4) Drinkability")
            print(f"(5) Drink Now Wines!")
            print(f"(6) Too Late")

            cmd = input(f"\npress [M] to return to Cellar Management: ")
            if cmd.upper() == "M":
                break
            elif cmd in "123456":
                if cmd == "1":
                    if not(debug):
                        appMenu.clear_screen()

                    print(f"Wine List")
                    print(f"{'-' * 88}")
                    print(f"\t #\tQty\tYear\tWine Name")
                    print(f"\t{'-' * 80}")
                    print(app.accounts[app.active_account])
                    print(f"\t{'-' * 80}")
                    input("\nPress [Enter] to continue")

                if cmd == "2":
                    if not(debug):
                        appMenu.clear_screen()
                    print(f"Wine Detail Cards")
                    for bottle in app.accounts[app.active_account].bottles.values():
                        print(bottle)
                    print(f"{'-' * 60}\n")
                    input("\nPress [Enter] to continue")

                if cmd == "3":
                    if not(debug):
                        appMenu.clear_screen()
                    wine_symbol = " X "

                    with open(customer_file, 'rt', newline='') as f:
                        reader = csv.reader(f)
                        next(reader, None)
                        for row in reader:
                            if app.active_account == row[2].lower():
                                max_rows = int(row[4])
                                max_cols = int(row[5])

                    cellar_grid = [[' . ' for j in range(0, max_cols)] for i in range(0, max_rows)]
                    for entry in app.accounts[app.active_account].bottles.values():
                        if (entry.row <= max_rows) or (entry.col <= max_cols):
                            cellar_grid[int(entry.row)][int(entry.col)] = wine_symbol

                    print(f"Cellar Grid View")
                    print(f"{'-' * (max_cols * 3 + 5)}\n")
                    print("     ", end="")
                    for col_nums in range(1, max_cols + 1):
                        print(format(str(col_nums), '^3s'), end="")
                    print()
                    print(f"{'_' * (max_cols * 3 + 5)}")

                    for i in range(0, max_rows):
                        print(format(str(i + 1) + " |", '>5s'), end="")
                        for j in range(0, max_cols):
                            print(cellar_grid[i][j], end="")
                        print()
                    print(f"\n{'-' * (max_cols * 3 + 5)}")
                    input("\nPress [Enter] to continue")

                if cmd == "4":
                    if not(debug):
                        appMenu.clear_screen()
                    print(f"Wines Ready to be Consumed")
                    for bottle in app.accounts[app.active_account].bottles.values():
                        if bottle.beginConsume < currentYear and bottle.endConsume >= currentYear:
                            print(bottle)
                    print(f"{'-' * 60}\n")
                    input("\nPress [Enter] to continue")

                if cmd == "5":
                    if not(debug):
                        appMenu.clear_screen()
                    print(f"Drink Now Wines!")
                    for bottle in app.accounts[app.active_account].bottles.values():
                        if bottle.endConsume == currentYear:
                            print(bottle)
                    print(f"{'-' * 60}\n")
                    input("\nPress [Enter] to continue")

                if cmd == "6":
                    if not(debug):
                        appMenu.clear_screen()
                    print(f"Wines that are too old to drink")
                    for bottle in app.accounts[app.active_account].bottles.values():
                        if bottle.endConsume < currentYear:
                            print(bottle)
                    print(f"{'-' * 60}\n")
                    input("\nPress [Enter] to continue")
            else:
                input(f"\nInvalid entry. Press [Enter] to continue")

        appMenu.cellar_mgmt_menu()

# ##########################


app = App()
appMenu = Menu()
appMenu.main_menu()
