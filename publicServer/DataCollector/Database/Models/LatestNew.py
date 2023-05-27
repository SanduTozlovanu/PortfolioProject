from sqlalchemy import Column, String, Integer, Date
from datetime import datetime
from publicServer.DataCollector.Database.JsonAble import JsonAble
from publicServer.DataCollector.Database.base import Base


class LatestNew(Base, JsonAble):
    __tablename__ = "latestNews"
    id = Column("id", Integer, primary_key=True)
    date = Column("date", Date, nullable=False)
    ticker = Column("ticker", String, nullable=False)
    title = Column("title", String, unique=True)
    image = Column("image", String, nullable=False)
    site = Column("site", String, nullable=False)
    text = Column("text", String, unique=True)
    url = Column("url", String, nullable=False)

    def __init__(self, ticker: str, title: str, image: str, site: str, text: str, url: str, date: str):
        self.ticker: str = ticker
        self.title: str = title
        self.image: str = image
        self.site: str = site
        self.text: str = text
        self.url: str = url
        self.date: datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"({self.id} {self.ticker} {self.title} {self.image} {self.site} {self.text} {self.url})"
