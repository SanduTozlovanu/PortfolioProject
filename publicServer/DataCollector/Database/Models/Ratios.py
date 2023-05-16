from sqlalchemy import Column, String, Integer, Float

from publicServer.DataCollector.Database.JsonAble import JsonAble
from publicServer.DataCollector.Database.base import Base


class Ratios(Base, JsonAble):
    __tablename__ = "ratios"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, nullable=False)
    ebtPerEbit = Column("ebtPerEbit", Float, nullable=False)
    netProfitMargin = Column("netProfitMargin", Float, nullable=False)
    operatingProfitMargin = Column("operatingProfitMargin", Float, nullable=False)
    priceToBookRatio = Column("priceToBookRatio", Float, nullable=False)

    def __init__(self, ticker: str, ebtPerEbit: float, netProfitMargin: float, operatingProfitMargin: float, priceToBookRatio:float):
        self.ticker: str = ticker
        self.ebtPerEbit: float = ebtPerEbit
        self.netProfitMargin: float = netProfitMargin
        self.operatingProfitMargin: float = operatingProfitMargin
        self.priceToBookRatio: float = priceToBookRatio

    def update(self, object):
        self.ticker: str = object.ticker
        self.ebtPerEbit: float = object.ebtPerEbit
        self.netProfitMargin: float = object.netProfitMargin
        self.operatingProfitMargin: float = object.operatingProfitMargin
        self.priceToBookRatio: float = object.priceToBookRatio

