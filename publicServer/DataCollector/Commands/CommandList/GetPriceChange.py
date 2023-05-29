from abc import ABC

import requests

from publicServer.DataCollector.Commands.Command import Command
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.StockPrice import StockPrice
from publicServer.DataCollector.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_MINUTE
from publicServer.config.definitions import KEY_URL


class GetPriceChange(Command, ABC):
    def __init__(self):
        super().__init__(ONE_MINUTE, 2, 1)
        self.url = API_ENDPOINT + "v3/stock-price-change/{}?" + KEY_URL

    def execute(self):
        self.prepareRequest()
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json())
        else:
            print(f"[GetPriceChange] failed to get stock price change {result.status_code}")

    def prepareRequest(self):
        ticker_list = ""
        for ticker in db.query(Company.ticker).all():
            ticker_list += ticker[0] + ","
        self.url = self.url.format(ticker_list[:-1])

    @staticmethod
    def collectData(result):
        for elem in result:
            stock_price_change = StockPrice(ticker=elem["symbol"], price=0, change=elem["1D"], yearChange=elem["1Y"])
            result: StockPrice = db.query(StockPrice).filter(StockPrice.ticker == stock_price_change.ticker).first()
            if result:
                result.change = stock_price_change.change
                result.yearChange = stock_price_change.yearChange
                result.update(result)
            else:
                db.add(stock_price_change)
        db.commit()
