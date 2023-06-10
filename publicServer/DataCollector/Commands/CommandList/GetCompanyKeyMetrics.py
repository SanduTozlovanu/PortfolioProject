from abc import ABC

import requests

from publicServer.DataCollector.Commands.Command import Command
from publicServer.Database.Models.Company import Company
from publicServer.Database.Models.KeyMetrics import KeyMetrics
from publicServer.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_MINUTE
from publicServer.config.definitions import KEY_URL


class GetCompanyKeyMetrics(Command, ABC):
    def __init__(self):
        super().__init__(ONE_MINUTE, 6, 10)
        self.url = API_ENDPOINT + "v3/key-metrics/{}?limit=1&period=quarter&" + KEY_URL

    def execute(self):
        collect_list = []
        for ticker in db.query(Company.ticker).all():
            ticker = ticker.ticker
            statement = db.query(KeyMetrics).filter(KeyMetrics.ticker == ticker).first()
            if not statement:
                collect_list.append(ticker)
                if len(collect_list) >= self.rate_cost:
                    break
        for i in range(0, len(collect_list)):
            self.prepareRequest(i, collect_list)
            result = requests.get(self.url)
            if result.status_code == 200:
                self.collectData(result.json())
            else:
                print(f"[GetCompanyKeyMetrics] failed to get company key metrics {result.status_code}")
                return

    def prepareRequest(self, index, collecting_list):
        self.url = API_ENDPOINT + "v3/key-metrics/{}?limit=1&period=quarter&" + KEY_URL
        self.url = self.url.format(collecting_list[index])

    @staticmethod
    def collectData(result):
        for metricsResult in result:
            key_metric = KeyMetrics(ticker=metricsResult["symbol"], peRatio=metricsResult["peRatio"],
                                    priceToSalesRatio=metricsResult["priceToSalesRatio"],
                                    freeCashFlowYield=metricsResult["freeCashFlowYield"],
                                    enterpriseValueOverEBITDA=metricsResult["enterpriseValueOverEBITDA"])
            db.add(key_metric)
        db.commit()
