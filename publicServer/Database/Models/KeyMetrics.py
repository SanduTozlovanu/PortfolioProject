from sqlalchemy import Column, String, Integer, Float

from publicServer.Database.JsonAble import JsonAble
from publicServer.Database.base import Base


class KeyMetrics(Base, JsonAble):
    __tablename__ = "keyMetrics"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, nullable=False)
    peRatio = Column("peRatio", Float, nullable=False)
    priceToSalesRatio = Column("priceToSalesRatio", Float, nullable=False)
    freeCashFlowYield = Column("freeCashFlowYield", Float, nullable=False)
    enterpriseValueOverEBITDA = Column("enterpriseValueOverEBITDA", Float, nullable=False)

    def __init__(self, ticker: str, peRatio: float, priceToSalesRatio: float, freeCashFlowYield: float,
                 enterpriseValueOverEBITDA: float):
        self.ticker: str = ticker
        if not peRatio:
            self.peRatio: float = 0
        else:
            self.peRatio: float = peRatio
        if not priceToSalesRatio:
            self.priceToSalesRatio: float = 0
        else:
            self.priceToSalesRatio: float = priceToSalesRatio
        if not freeCashFlowYield:
            self.freeCashFlowYield: float = 0
        else:
            self.freeCashFlowYield: float = freeCashFlowYield
        if not enterpriseValueOverEBITDA:
            self.enterpriseValueOverEBITDA: float = 0
        else:
            self.enterpriseValueOverEBITDA: float = enterpriseValueOverEBITDA

    def update(self, object):
        self.ticker: str = object.ticker
        if not object.peRatio:
            self.peRatio: float = 0
        else:
            self.peRatio: float = object.peRatio
        if not object.priceToSalesRatio:
            self.priceToSalesRatio: float = 0
        else:
            self.priceToSalesRatio: float = object.priceToSalesRatio
        if not object.freeCashFlowYield:
            self.freeCashFlowYield: float = 0
        else:
            self.freeCashFlowYield: float = object.freeCashFlowYield
        if not object.enterpriseValueOverEBITDA:
            self.enterpriseValueOverEBITDA: float = 0
        else:
            self.enterpriseValueOverEBITDA: float = object.enterpriseValueOverEBITDA

