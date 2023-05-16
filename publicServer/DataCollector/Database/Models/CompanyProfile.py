from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey

from publicServer.DataCollector.Database.JsonAble import JsonAble
from publicServer.DataCollector.Database.base import Base


class CompanyProfile(Base, JsonAble):
    __tablename__ = "companyProfiles"
    ticker = Column("ticker", String, ForeignKey("companies.ticker"), primary_key=True)
    price = Column("price", Float, nullable=False)
    volAvg = Column("volAvg", Integer, nullable=False)
    beta = Column("beta", Float, nullable=False)
    mktCap = Column("mktCap", Integer, nullable=False)
    companyName = Column("companyName", String, nullable=False)
    exchange = Column("exchange", String, nullable=False)
    industry = Column("industry", String, nullable=False)
    sector = Column("sector", String, nullable=False)
    website = Column("website", String, nullable=False)
    description = Column("description", String, nullable=False)
    ceo = Column("ceo", String, nullable=False)
    fullTimeEmployees = Column("fullTimeEmployees", Integer, nullable=False)
    image = Column("image", String, nullable=False)
    ipoDate = Column("ipoDate", Date)

    def __init__(self, ticker: String, price: float, volAvg: int, beta: float, mktCap: int, companyName: str,
                 exchange: str, industry: str, sector: str, website: str, description: str, ceo: str,
                 fullTimeEmployees: int, image: str, ipoDate: datetime.date):
        self.ticker = ticker
        self.price = price
        self.volAvg = volAvg
        self.beta = beta
        self.mktCap = mktCap
        self.companyName = companyName
        self.exchange = exchange
        self.industry = industry
        self.sector = sector
        self.website = website
        self.description = description
        self.ceo = ceo
        self.fullTimeEmployees = fullTimeEmployees
        self.image = image
        self.ipoDate = ipoDate

    def update(self, object):
        self.ticker: str = object.ticker
        self.price: float = object.price
        self.volAvg: int = object.volAvg
        self.beta: float = object.beta
        self.mktCap: int = object.mktCap
        self.companyName: str = object.companyName
        self.exchange: str = object.exchange
        self.industry: str = object.industry
        self.website: str = object.website
        self.sector: str = object.sector
        self.description: str = object.description
        self.ceo: str = object.ceo
        self.fullTimeEmployees: int = object.fullTimeEmployees
        self.image: str = object.image
        self.ipoDate: datetime.date = object.ipoDate

    def __repr__(self):
        return f"({self.ticker} {self.price} {self.volAvg} {self.mktCap} {self.companyName}" \
               f"{self.exchange} {self.industry} {self.website} {self.description} {self.ceo}" \
               f"{self.fullTimeEmployees} {self.image} {self.ipoDate})"
