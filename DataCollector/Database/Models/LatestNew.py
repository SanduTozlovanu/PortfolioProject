from sqlalchemy import Column, String, Integer
from DataCollector.Database.base import Base


class LatestNew(Base):
    __tablename__ = "latestNews"
    id = Column("id", Integer, primary_key=True)
    ticker = Column("ticker", String, nullable=False)
    title = Column("title", String, nullable=False)
    image = Column("image", String, nullable=False)
    site = Column("site", String, nullable=False)
    text = Column("text", String, nullable=False)
    url = Column("url", String, nullable=False)

    def __init__(self, ticker: str, title: str, image: str, site: str, text: str, url: str):
        self.ticker: str = ticker
        self.title: str = title
        self.image: str = image
        self.site: str = site
        self.text: str = text
        self.url: str = url

    def update(self, object):
        self.ticker: str = object.ticker
        self.title: str = object.title
        self.image: str = object.image
        self.site: str = object.site
        self.text: str = object.text
        self.url: str = object.url

    def __repr__(self):
        return f"({self.id} {self.ticker} {self.title} {self.image} {self.site} {self.text} {self.url})"
