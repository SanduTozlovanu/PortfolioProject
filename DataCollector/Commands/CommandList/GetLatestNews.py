from abc import ABC

import requests
from sqlalchemy.exc import OperationalError

from DataCollector.Commands.Command import Command
from DataCollector.Database.Models.LatestNew import LatestNew
from DataCollector.Database.session import db
from DataCollector.config.constants import API_ENDPOINT, TEN_MINUTES
from DataCollector.config.definitions import KEY_URL


class GetLatestNews(Command, ABC):
    def __init__(self):
        super().__init__(TEN_MINUTES, 5, 1)
        self.url = API_ENDPOINT + "v3/stock_news?limit=10&" + KEY_URL

    def execute(self):
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json())
        else:
            print(f"[GetLatestNews] failed to get latest news {result.status_code}")

    @staticmethod
    def collectData(result):
        try:
            db.query(LatestNew).delete()
        except OperationalError as exc:
            print(exc.args)
        print(db.query(LatestNew).all())
        for new in result:
            new_to_insert = LatestNew(ticker=new["symbol"], title=new["title"], image=new["image"],
                                      site=new["site"], text=new["text"], url=new["url"])
            db.add(new_to_insert)
        db.commit()
