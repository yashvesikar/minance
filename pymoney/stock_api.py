import requests
from typing import Dict
from abc import ABC, abstractmethod

import finnhub

API_KEY = 'c15d84v48v6tvr5kh920'
SANDBOX_KEY = 'sandbox_c15d84v48v6tvr5kh92g'


class API(ABC):
    def __init__(self, sandbox=False):
        self.session = requests.Session()
        self.session.auth = ('X-Finnhub-Token', SANDBOX_KEY if sandbox else API_KEY)

    @abstractmethod
    def quote(self, ticker: str) -> Dict[str, float]:
        pass


class FinnHub(API):
    def __init__(self, sandbox=True):
        super().__init__(sandbox)
        self.client = finnhub.Client(api_key=f"{SANDBOX_KEY if sandbox else API_KEY}")

    def quote(self, ticker: str) -> Dict[str, float]:
        q = self.client.quote(ticker)
        d = {'open': q['o'], 'high': q['h'], 'low': q['l'], 'current': q['c']} if q else None

        return d
