from abc import ABC

import requests

from publicServer.DataCollector.Commands.Command import Command
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.StockPrice import StockPrice
from publicServer.DataCollector.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_MINUTE
from publicServer.config.definitions import KEY_URL


class GetStockPrice(Command, ABC):
    def __init__(self):
        super().__init__(ONE_MINUTE, 2, 1)
        self.url = API_ENDPOINT + "v3/quote-short/{}?" + KEY_URL

    def execute(self):
        self.prepareRequest()
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json())
        else:
            print(f"[GetStockPrice] failed to get stock price {result.status_code}")

    def prepareRequest(self):
        ticker_list = ""
        for ticker in db.query(Company.ticker).all():
            ticker_list += ticker[0] + ","
        self.url = self.url.format(ticker_list[:-1])

    @staticmethod
    def collectData(result):
        for elem in result:
            stock_price = StockPrice(ticker=elem["symbol"], price=elem["price"])
            result: StockPrice = db.query(StockPrice).filter(StockPrice.ticker == stock_price.ticker).first()
            if result:
                result.update(stock_price)
            else:
                db.add(stock_price)
        db.commit()
