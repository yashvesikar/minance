import time

from .stock_api import FinnHub


class MockAccount:
    def __init__(self, initial_value=1000, sandbox=True, testing=False):
        self.balance = initial_value
        # {ticker: {amount, cost, cost basis}}
        self.testing = testing
        self.portfolio = {}
        self.client = FinnHub(sandbox=sandbox)
        self.transaction_count = 0
        date = time.strftime('%m_%d_%Y')
        if not testing:
            self.log_file = open(f'logs/{date}.csv', 'w')

    def log(self, transaction: str):
        if not self.testing:
            self.log_file.write(f'{transaction},{self.balance}\n')
            self.transaction_count += 1
            if self.transaction_count % 10 == 0:
                self.log_file.write(f'VALUE,{self.value()}\n')

    def value(self):
        return \
            self.balance + \
            sum([self.client.quote(t)['current'] * self.portfolio[t]['amount'] for t in self.portfolio.keys()])

    def buy(self, amount, ticker) -> float:
        """
        Return value is always quote
        """
        q = self.client.quote(ticker)['current']
        cost = amount * q
        print(f'Buy {amount} {ticker} at {q} for {cost}')

        if cost > self.balance:
            print(f'Too Expensive: {cost} is greater than balance {self.balance}')
            return q

        # print(f'Old portfolio: {self.portfolio}')
        if ticker in self.portfolio:

            _amount = self.portfolio[ticker]['amount']
            self.portfolio[ticker]['amount'] += amount
            _value = self.portfolio[ticker]['value']
            self.portfolio[ticker]['value'] += cost
            _cb = self.portfolio[ticker]['cb']

            # cb = ((_cb * _a) + (amt * c))/(new_amt)
            self.portfolio[ticker]['cb'] = ((_cb * _amount) + (amount * cost)) / (self.portfolio[ticker]['amount'])
        else:
            self.portfolio[ticker] = {'amount': amount, 'value': cost, 'cb': cost/amount}

        self.balance -= cost
        transaction = f'BUY,{time.time()},{ticker},{amount},{q}'
        self.log(transaction)
        # print(f'New portfolio: {self.portfolio}')

        return q

    def sell(self, amount, ticker) -> float:
        """
        Return value is always the quote
        """
        q = self.client.quote(ticker)['current']
        ret = amount * q
        print(f'Sell {amount} {ticker} at {q} for {ret}')

        # print(f'Old portfolio: {self.portfolio}')
        if ticker in self.portfolio:
            _position = self.portfolio[ticker]['amount']

            if amount > _position:
                print(f'Not enough shares: cannot sell {amount} is greater than position {_position}')
                return q

            self.portfolio[ticker]['amount'] -= amount
            _value = self.portfolio[ticker]['value']
            self.portfolio[ticker]['value'] -= ret

            self.balance += ret

            if amount == _position:
                del self.portfolio[ticker]
                return q

            transaction = f'SELL,{time.time()},{ticker},{amount},{q}'
            self.log(transaction)

        else:
            print(f'No position in {ticker}')

        return q
