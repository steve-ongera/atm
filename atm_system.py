import random
from datetime import datetime

class Account:
    def __init__(self, username, pin, initial_balance=0):
        self.username = username
        self.pin = pin
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._log_transaction('Deposit', amount)
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._log_transaction('Withdrawal', -amount)
            return True
        return False

    def _log_transaction(self, type, amount):
        transaction = {
            'type': type,
            'amount': amount,
            'balance': self.balance,
            'timestamp': datetime.now()
        }
        self.transactions.append(transaction)

class ATM:
    def __init__(self):
        self.accounts = {}
        self.logged_in_user = None

    def register(self, username, pin):
        if username in self.accounts:
            return False
        self.accounts[username] = Account(username, pin)
        return True

    def login(self, username, pin):
        account = self.accounts.get(username)
        if account and account.pin == pin:
            self.logged_in_user = account
            return True
        return False

    def logout(self):
        self.logged_in_user = None

    def get_balance(self):
        return self.logged_in_user.balance if self.logged_in_user else None

    def deposit(self, amount):
        return self.logged_in_user.deposit(amount) if self.logged_in_user else False

    def withdraw(self, amount):
        return self.logged_in_user.withdraw(amount) if self.logged_in_user else False

    def change_pin(self, new_pin):
        if self.logged_in_user:
            self.logged_in_user.pin = new_pin
            return True
        return False

    def get_transactions(self):
        return self.logged_in_user.transactions if self.logged_in_user else []

def main():
    atm = ATM()

    while True:
        print("\n--- ATM System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            username = input("Create Username: ")
            pin = input("Create PIN: ")
            if atm.register(username, pin):
                print("Registration Successful!")
            else:
                print("Username already exists.")

        elif choice == '2':
            username = input("Username: ")
            pin = input("PIN: ")
            if atm.login(username, pin):
                while True:
                    print("\n--- Banking Menu ---")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transaction History")
                    print("5. Change PIN")
                    print("6. Logout")
                    
                    menu_choice = input("Enter choice: ")
                    
                    if menu_choice == '1':
                        print(f"Balance: ${atm.get_balance()}")
                    
                    elif menu_choice == '2':
                        amount = float(input("Deposit Amount: $"))
                        if atm.deposit(amount):
                            print("Deposit Successful!")
                        else:
                            print("Invalid Amount")
                    
                    elif menu_choice == '3':
                        amount = float(input("Withdrawal Amount: $"))
                        if atm.withdraw(amount):
                            print("Withdrawal Successful!")
                        else:
                            print("Insufficient Funds")
                    
                    elif menu_choice == '4':
                        transactions = atm.get_transactions()
                        for t in transactions:
                            print(f"{t['timestamp']} | {t['type']}: ${abs(t['amount'])}")
                    
                    elif menu_choice == '5':
                        new_pin = input("Enter New PIN: ")
                        if atm.change_pin(new_pin):
                            print("PIN Changed Successfully!")
                    
                    elif menu_choice == '6':
                        atm.logout()
                        break
            else:
                print("Invalid Login")

        elif choice == '3':
            break

if __name__ == "__main__":
    main()