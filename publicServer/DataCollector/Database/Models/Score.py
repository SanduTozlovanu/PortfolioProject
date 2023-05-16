from sqlalchemy import Column, String, Integer, Float

from publicServer.DataCollector.Database.JsonAble import JsonAble
from publicServer.DataCollector.Database.base import Base


class Score(Base, JsonAble):
    __tablename__ = "scores"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, nullable=False)
    altmanZScore = Column("altmanZScore", Float, nullable=False)
    piotroskiScore = Column("piotroskiScore", Integer, nullable=False)

    def __init__(self, ticker: str, piotroskiScore: int, altmanZScore: float):
        self.ticker: str = ticker
        self.piotroskiScore: int = piotroskiScore
        self.altmanZScore: float = altmanZScore

    def update(self, object):
        self.ticker: str = object.ticker
        self.piotroskiScore: str = object.piotroskiScore
        self.altmanZScore: str = object.altmanZScore

