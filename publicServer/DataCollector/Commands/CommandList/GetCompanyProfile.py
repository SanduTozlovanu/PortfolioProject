from abc import ABC


import requests
from datetime import datetime
from publicServer.DataCollector.Commands.Command import Command
from publicServer.DataCollector.Database.Models.Company import Company
from publicServer.DataCollector.Database.Models.CompanyProfile import CompanyProfile
from publicServer.DataCollector.Database.session import db
from publicServer.config.constants import API_ENDPOINT, ONE_DAY
from publicServer.config.definitions import KEY_URL


class GetCompanyProfile(Command, ABC):
    def __init__(self):
        super().__init__(ONE_DAY, 2, 1)
        self.url = API_ENDPOINT + "v3/profile/{}?" + KEY_URL

    def execute(self):
        self.prepareRequest()
        result = requests.get(self.url)
        if result.status_code == 200:
            self.collectData(result.json())
        else:
            print(f"[GetCompanyProfile] failed to get company profile {result.status_code}")

    def prepareRequest(self):
        ticker_list = ""
        for ticker in db.query(Company.ticker).all():
            ticker_list += ticker[0] + ","
        self.url = self.url.format(ticker_list[:-1])

    @staticmethod
    def collectData(result):
        for profile in result:
            try:
                ipo_date = datetime.strptime(profile["ipoDate"], '%Y-%m-%d')
            except ValueError:
                ipo_date = None

            com_profile = CompanyProfile(ticker=profile["symbol"], companyName=profile["companyName"],
                                         description=profile["description"], exchange=profile["exchange"],
                                         fullTimeEmployees=profile["fullTimeEmployees"], image=profile["image"],
                                         industry=profile["industry"], sector=profile["sector"], price=profile["price"],
                                         ceo=profile["ceo"], ipoDate=ipo_date, website=profile["website"],
                                         mktCap=profile["mktCap"], volAvg=profile["volAvg"], beta=profile["beta"])
            result: CompanyProfile = db.query(CompanyProfile).filter(CompanyProfile.ticker == com_profile.ticker).first()
            if result:
                result.update(com_profile)
            else:
                db.add(com_profile)
        db.commit()
