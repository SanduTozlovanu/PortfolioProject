from sqlalchemy import Column, String, Integer

from publicServer.Database.JsonAble import JsonAble
from publicServer.Database.base import Base


class PricePrediction(Base, JsonAble):
    __tablename__ = "pricePredictions"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, nullable=False)
    jsonData = Column("jsonData", String, nullable=False)

    def __init__(self, jsonData: str, ticker: str):
        self.jsonData: str = jsonData
        self.ticker: str = ticker

    def update(self, object):
        self.jsonData: str = object.jsonData
        self.ticker: str = object.ticker

