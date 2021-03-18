import unittest

from pymoney.mock_account import MockAccount
from pymoney.stock_api import FinnHub


class TestMockAccount(unittest.TestCase):

    def setUp(self):
        self.account = MockAccount(testing=True)
        self.client = FinnHub(sandbox=True)

    def test_setup(self):
        self.assertEqual(1000, self.account.balance)
        self.assertEqual({}, self.account.portfolio)

    def test_buy(self):
        aapl_ticker = 'AAPL'
        aapl_quote = self.client.quote(aapl_ticker)['current']
        starting_balance = 1000
        self.assertEqual(starting_balance, self.account.balance)
        
        self.account.buy(2, 'AAPL')
        self.assertEqual(starting_balance - (aapl_quote * 2), self.account.balance)
        self.assertEqual({'amount': 2, 'value': 2 * aapl_quote, 'cb': aapl_quote}, self.account.portfolio['AAPL'])


    def test_sell(self):
        # This test is kind of bogus(ish) since it assumes that the price of the security remains constant across the duration of the test which of course is not a guarantee
        aapl_ticker = 'AAPL'
        aapl_quote = self.client.quote(aapl_ticker)['current']
        starting_balance = 1000
        self.assertEqual(starting_balance, self.account.balance)

        # Buy 2 shares        
        self.account.buy(2, 'AAPL')
        new_balance = starting_balance - (aapl_quote * 2)
        self.assertEqual(new_balance, self.account.balance)
        self.assertEqual({'amount': 2, 'value': 2 * aapl_quote, 'cb': aapl_quote}, self.account.portfolio['AAPL'])

        # Sell 1 share
        self.account.sell(1, 'AAPL')
        new_balance = new_balance + aapl_quote  
        self.assertEqual(new_balance, self.account.balance)
        self.assertEqual({'amount': 1, 'value': aapl_quote, 'cb': aapl_quote}, self.account.portfolio['AAPL'])

        # Sell 1 share
        self.account.sell(1, 'AAPL')
        new_balance = new_balance + aapl_quote
        self.assertEqual(new_balance, self.account.balance)
        self.assertEqual(None, self.account.portfolio.get('AAPL'))


if __name__ == '__main__':
    unittest.main()
