from abc import ABC

import requests

from publicServer.DataCollector.Commands.Command import Command
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.Score import Score
from publicServer.DataCollector.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_MINUTE
from publicServer.config.definitions import KEY_URL


class GetCompanyScore(Command, ABC):
    def __init__(self):
        super().__init__(ONE_MINUTE, 6, 10)
        self.url = API_ENDPOINT + "v4/score?symbol={}&" + KEY_URL

    def execute(self):
        collect_list = []
        for ticker in db.query(Company.ticker).all():
            ticker = ticker.ticker
            statement = db.query(Score).filter(Score.ticker == ticker).first()
            if not statement:
                collect_list.append(ticker)
                if len(collect_list) >= self.rate_cost:
                    break
        for i in range(0, len(collect_list)):
            self.prepareRequest(i, collect_list)
            result = requests.get(self.url)
            if result.status_code == 200:
                self.collectData(result.json(), collect_list[i])
            else:
                print(f"[GetCompanyScore] failed to get company score {result.status_code}")
                return

    def prepareRequest(self, index, collecting_list):
        self.url = API_ENDPOINT + "v4/score?symbol={}&" + KEY_URL
        self.url = self.url.format(collecting_list[index])

    @staticmethod
    def collectData(result, ticker):
        for scoreResult in result:
            score = Score(ticker=scoreResult["symbol"], altmanZScore=scoreResult["altmanZScore"],
                          piotroskiScore=scoreResult['piotroskiScore'])
            db.add(score)
        if len(result) == 0:
            score = Score(ticker=ticker, altmanZScore=5.64,
                          piotroskiScore=5)
            db.add(score)
        db.commit()
