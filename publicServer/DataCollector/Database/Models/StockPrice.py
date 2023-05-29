from sqlalchemy import Column, String, Integer, Float

from publicServer.DataCollector.Database.JsonAble import JsonAble
from publicServer.DataCollector.Database.base import Base


class StockPrice(Base, JsonAble):
    __tablename__ = "stockPrice"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, unique=True)
    price = Column("price", Float, nullable=False)
    change = Column("change", Float, nullable=True)
    yearChange = Column("yearChange", Float, nullable=True)

    def __init__(self, ticker: str, price: float, change: float, yearChange: float):
        self.ticker: str = ticker
        self.price: float = price
        self.change: float = change
        self.yearChange: float = yearChange

    def update(self, object):
        self.ticker: str = object.ticker
        self.price: str = object.price
        self.change: float = object.change
        self.yearChange: float = object.yearChange

