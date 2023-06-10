from sqlalchemy import Column, String, Integer

from publicServer.Database.JsonAble import JsonAble
from publicServer.Database.base import Base


class Balance(Base, JsonAble):
    __tablename__ = "balances"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, nullable=False)
    totalInvestments = Column("totalInvestments", Integer, nullable=False)
    totalDebt = Column("totalDebt", Integer, nullable=False)
    totalCash = Column("totalCash", Integer, nullable=False)

    def __init__(self, ticker: str, totalInvestments: int, totalDebt: int, totalCash: int):
        self.ticker: str = ticker
        self.totalInvestments: int = totalInvestments
        self.totalDebt: int = totalDebt
        self.totalCash: int = totalCash

    def update(self, object):
        self.ticker: str = object.ticker
        self.totalInvestments: int = object.totalInvestments
        self.totalDebt: int = object.totalDebt
        self.totalCash: int = object.totalCash

