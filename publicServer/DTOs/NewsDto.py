from datetime import datetime


class NewsDto:
    def __init__(self, image: str, date: datetime, title: str, text: str, ticker: str, url: str, change: float, site: str):
        self.image = image
        self.date = date.strftime("%Y-%m-%d")
        self.title = title
        if len(text) > 210:
            text = text[:213] + "..."
        self.text = text
        self.ticker = ticker
        self.url = url
        self.change = str(round(change, 2))
        self.site = site
