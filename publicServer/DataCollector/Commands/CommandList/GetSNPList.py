from abc import ABC

import requests

from publicServer.DataCollector.Commands.Command import Command
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_DAY
from publicServer.config.definitions import KEY_URL


class GetSNPList(Command, ABC):
    def __init__(self):
        super().__init__(ONE_DAY, 5, 1)
        self.url = API_ENDPOINT + "v3/sp500_constituent?" + KEY_URL

    def execute(self):
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json())
        else:
            print(f"[GetSNPList] failed to get SNP list {result.status_code}")

    @staticmethod
    def collectData(result):
        for company in result:
            company_to_insert = Company(company["symbol"], company["name"], company["sector"],
                                        company["subSector"], company["headQuarter"], company["founded"])
            result: Company = db.query(Company).filter(Company.ticker == company_to_insert.ticker).first()
            if result:
                result.update(company_to_insert)
            else:
                db.add(company_to_insert)
        db.commit()
