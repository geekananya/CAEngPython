import requests

# bank_account.py
class BankAccount:
    def __init__(self, acct_number, balance=0):
        self.balance = balance
        self.acct_number = acct_number

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient amt")
        self.balance -= amount

    def get_balance(self):
        return self.balance

    def get_owner_email(self):
        resp = requests.get(f'https://dummyjson.com/users/{self.acct_number}')
        if resp.ok :
            return f'{self.acct_number}:{resp.text}'
        else :
            return 'Bad Response!'


# ob = BankAccount(1)
# print(ob.get_owner_email())