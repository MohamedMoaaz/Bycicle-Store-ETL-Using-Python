from utilities.logger import Logger
import requests
import pandas as pd
from urllib.parse import urlparse

class ExchangeRateFetcher:
    def __init__(self, api_url):
        self.api_url = api_url
        self.logger = Logger()

    def fetch_exchange_rates(self):
        url = self.api_url
        domain = urlparse(self.api_url).netloc.split('.')[0]
        response = requests.get(url)
        data = response.json()
        rates = data["rates"]
        df = pd.DataFrame(list(rates.items()), columns=["currency", "rate"])
        self.logger.log(f"  Fetched {len(df)} exchange rates from {domain}")
        return df