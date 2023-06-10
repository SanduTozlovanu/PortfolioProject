from abc import ABC

import requests
from sqlalchemy.exc import OperationalError

from publicServer.DataCollector.Commands.Command import Command
from publicServer.Database.Models.Company import Company
from publicServer.Database.Models.LatestNew import LatestNew
from publicServer.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_HOUR
from publicServer.config.definitions import KEY_URL


class GetLatestNews(Command, ABC):
    def __init__(self):
        super().__init__(ONE_HOUR, 5, 1)
        self.url = API_ENDPOINT + "v3/stock_news?tickers={}&page={}&" + KEY_URL
        print(self.url)

    def execute(self):
        self.prepareRequest("0")
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json(), True)
        else:
            print(f"[GetLatestNews] failed to get latest news {result.status_code}")

        self.prepareRequest("1")
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json(), False)
        else:
            print(f"[GetLatestNews] failed to get latest news {result.status_code}")

        self.prepareRequest("2")
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json(), False)
        else:
            print(f"[GetLatestNews] failed to get latest news {result.status_code}")

        self.prepareRequest("3")
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json(), False)
        else:
            print(f"[GetLatestNews] failed to get latest news {result.status_code}")

    def prepareRequest(self, page: str):
        self.url = API_ENDPOINT + "v3/stock_news?tickers={}&page={}&" + KEY_URL
        ticker_list = ""
        for ticker in db.query(Company.ticker).all():
            ticker_list += ticker[0] + ","
        self.url = self.url.format(ticker_list[:-1], page)

    @staticmethod
    def collectData(result, delete: bool):
        try:
            if delete:
                db.query(LatestNew).delete()
                db.commit()
        except OperationalError as exc:
            print(exc.args)
        for new in result:
            new_to_insert = LatestNew(ticker=new["symbol"], title=new["title"], image=new["image"],
                                      site=new["site"], text=new["text"], url=new["url"], date=new["publishedDate"])
            try:
                db.add(new_to_insert)
                db.commit()
            except Exception as e:
                db.rollback()
