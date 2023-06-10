from exceptions import NotFoundException
from publicServer.DTOs.NewsDto import NewsDto
from publicServer.Database.Models.LatestNew import LatestNew
from publicServer.Database.Models.StockPrice import StockPrice
from publicServer.Database.session import db


class NewsController:
    @staticmethod
    def receive_latest_new() -> NewsDto:
        new = db.query(LatestNew).order_by(LatestNew.date.desc()).first()
        news_dto = NewsDto(ticker=new.ticker, change=0, date=new.date, image=new.image,
                           text=new.text, url=new.url, title=new.title, site=new.site)
        return news_dto

    @staticmethod
    def receive_latest_news(ticker_list) -> list[NewsDto]:
        news_dtos: list[NewsDto] = []
        if ticker_list == "all":
            latest_news_list: list[LatestNew] = db.query(LatestNew).order_by(LatestNew.date.desc()).limit(40).all()
            for new in latest_news_list:
                stock_price: StockPrice = db.query(StockPrice).filter(StockPrice.ticker == new.ticker).first()
                if stock_price is None:
                    raise NotFoundException("Ticker stock price not found")
                news_dtos.append(
                    NewsDto(ticker=new.ticker, change=stock_price.change, date=new.date, image=new.image,
                            text=new.text, url=new.url, title=new.title, site=new.site))
        else:
            ticker_list = ticker_list.split(",")
            latest_news_list: list[LatestNew] = []
            titles_used = []
            for ticker in ticker_list:
                new_list = db.query(LatestNew).filter(LatestNew.ticker == ticker).order_by(
                    LatestNew.date.desc()).limit(
                    2).all()
                for new in new_list:
                    titles_used.append(new.title)
                latest_news_list += new_list
            latest_news_list += db.query(LatestNew).filter(LatestNew.title not in titles_used).order_by(
                LatestNew.date.desc()).limit(40 - len(latest_news_list)).all()
            for new in latest_news_list:
                stock_price: StockPrice = db.query(StockPrice).filter(StockPrice.ticker == new.ticker).first()
                if stock_price is None:
                    raise NotFoundException("Ticker stock price not found")
                news_dtos.append(
                    NewsDto(ticker=new.ticker, change=stock_price.change, date=new.date, image=new.image,
                            text=new.text, url=new.url, title=new.title, site=new.site))

        news_dtos.sort(key=lambda dto: dto.date, reverse=True)
        return news_dtos
