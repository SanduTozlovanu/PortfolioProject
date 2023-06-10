from sqlalchemy import Column, String, Integer

from publicServer.Database.JsonAble import JsonAble
from publicServer.Database.base import Base


class Company(Base, JsonAble):
    __tablename__ = "companies"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, unique=True)
    name = Column("name", String, nullable=False)
    sector = Column("sector", String, nullable=False)
    sub_sector = Column("sub_sector", String, nullable=False)
    head_quarter = Column("head_quarter", String, nullable=False)
    founded = Column("founded", Integer, nullable=False)

    def __init__(self, ticker: str, name: str, sector: str, sub_sector: str, head_quarter: str, founded: int):
        self.ticker: str = ticker
        self.name: str = name
        self.sector: str = sector
        self.sub_sector: str = sub_sector
        self.head_quarter: str = head_quarter
        self.founded: int = founded

    def update(self, object):
        self.ticker: str = object.ticker
        self.name: str = object.name
        self.sector: str = object.sector
        self.sub_sector: str = object.sub_sector
        self.head_quarter: str = object.head_quarter
        self.founded: int = object.founded

    def __repr__(self):
        return f"({self.id} {self.ticker} {self.name} {self.sector} {self.sub_sector} {self.head_quarter} {self.founded})"
