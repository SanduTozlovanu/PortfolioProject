from sqlalchemy import Column, String, Integer, Float

from publicServer.DataCollector.Database.JsonAble import JsonAble
from publicServer.DataCollector.Database.base import Base


class StockPrice(Base, JsonAble):
    __tablename__ = "stockPrice"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, unique=True)
    price = Column("price", Float, nullable=False)

    def __init__(self, ticker: str, price: float):
        self.ticker: str = ticker
        self.price: float = price

    def update(self, object):
        self.ticker: str = object.ticker
        self.price: str = object.price

