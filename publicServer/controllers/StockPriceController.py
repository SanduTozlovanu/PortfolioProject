from exceptions import NotFoundException
from publicServer.DTOs.StockPriceChangeDto import StockPriceChangeDto
from publicServer.DTOs.TickerPriceDto import TickerPriceDto
from publicServer.Database.Models.Company import Company
from publicServer.Database.Models.StockPrice import StockPrice
from publicServer.Database.session import db


class StockPriceController:
    @staticmethod
    def receive_top_loosers() -> list[TickerPriceDto]:
        losers_to_return = []
        stock_price_list: list[StockPrice] = db.query(StockPrice).order_by(StockPrice.change.asc()).limit(6).all()
        for stock_price in stock_price_list:
            losers_to_return.append(TickerPriceDto(stock_price.ticker, stock_price.change))
        return losers_to_return

    @staticmethod
    def receive_top_gainers() -> list[TickerPriceDto]:
        gainers_to_return = []
        stock_price_list: list[StockPrice] = db.query(StockPrice).order_by(StockPrice.change.desc()).limit(6).all()
        for stock_price in stock_price_list:
            gainers_to_return.append(TickerPriceDto(stock_price.ticker, stock_price.change))
        return gainers_to_return

    @staticmethod
    def receive_companies_price(company_list):
        response_dict = {}
        company_list = company_list.split(",")
        for company in company_list:
            price = db.query(StockPrice.price).filter(
                StockPrice.ticker == company).first()
            if price is None:
                raise NotFoundException("Company not found!")
            response_dict[company] = price["price"]
        return response_dict

    @staticmethod
    def receive_tickers_price_change(company_tickers) -> list[TickerPriceDto]:
        response_list = []
        company_list = company_tickers.split(",")
        for ticker in company_list:
            stockPrice = db.query(StockPrice).filter(
                StockPrice.ticker == ticker).first()
            if stockPrice is None:
                raise NotFoundException("Ticker not found!")
            response_list.append(TickerPriceDto(ticker, stockPrice.change))
        return response_list

    @staticmethod
    def receive_all_tickers_price_change() -> list[StockPriceChangeDto]:
        response_list: list[StockPriceChangeDto] = []
        company_list: list[Company] = db.query(Company).filter(Company.sector != "Energy").all()
        for company in company_list:
            stockPrice: StockPrice = db.query(StockPrice).filter(
                StockPrice.ticker == company.ticker).first()
            if stockPrice is None:
                continue
            response_list.append(
                StockPriceChangeDto(ticker=company.ticker, price=stockPrice.price, yearChange=stockPrice.yearChange))
        return response_list

