# test_bank_account.py
import unittest
from unittest.mock import patch
from bank_account import BankAccount

class TestBankAccount(unittest.TestCase):

    def setUp(self):                        # runs before each unit test case
        self.account = BankAccount(1, 100)
        self.account2 = BankAccount(5)

    def tearDown(self):
        del self.account
        del self.account2

    def test_initial_balance(self):
        self.assertEqual(self.account.get_balance(), 100)
        self.assertEqual(self.account2.get_balance(), 0)

    def test_deposit(self):
        self.account.deposit(50)
        self.account2.deposit(30)

        self.assertEqual(self.account.get_balance(), 150)
        self.assertEqual(self.account2.get_balance(), 30)

        with self.assertRaises(ValueError) as exc:
            self.account.deposit(-20)
        self.assertEqual(str(exc.exception), "Deposit amount must be positive")

    def test_withdraw(self):
        self.account.withdraw(30)

        self.assertEqual(self.account.get_balance(), 70)

        with self.assertRaises(ValueError) as exc:
            self.account.withdraw(200)
        self.assertEqual(str(exc.exception), "Insufficient amt")

        with self.assertRaises(ValueError) as exc:
            self.account.withdraw(-10)
        self.assertEqual(str(exc.exception), "Withdrawal amount must be positive")

        with self.assertRaises(ValueError) as exc:
            self.account2.withdraw(0)
        self.assertEqual(str(exc.exception), "Withdrawal amount must be positive")

    def test_get_owner_email(self):

        with patch('bank_account.requests.get') as mock_get:         # get is function that hits end point, provide it return val
            mock_get.return_value.ok = True
            mock_get.return_value.text = 'email@abc.com'

            em = self.account.get_owner_email()
            # assert
            mock_get.assert_called_with('https://dummyjson.com/users/1')
            self.assertEqual(em, '1:email@abc.com')

            mock_get.return_value.ok = False
            em = self.account2.get_owner_email()

            mock_get.assert_called_with('https://dummyjson.com/users/5')
            self.assertEqual(em, 'Bad Response!')

if __name__ == '__main__':
    unittest.main()
