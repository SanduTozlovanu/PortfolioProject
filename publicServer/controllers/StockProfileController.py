from exceptions import NotFoundException
from publicServer.DTOs.CompanySelectDataDto import CompanySelectDataDto
from publicServer.DTOs.StockBasedataDto import StockBasedataDto
from publicServer.Database.Models.Company import Company
from publicServer.Database.Models.CompanyProfile import CompanyProfile
from publicServer.Database.Models.StockPrice import StockPrice
from publicServer.Database.session import db


class StockProfileController:
    @staticmethod
    def receive_ticker_list():
        companies: list[Company] = db.query(Company).all()
        ticker_list = []
        for company in companies:
            ticker_list.append(company.ticker)
        return ticker_list

    @staticmethod
    def receive_stocks_basedata() -> list[StockBasedataDto]:
        companies: list[CompanyProfile] = db.query(CompanyProfile).join(Company).filter(Company.sector != "Energy").all()
        returned_companies: list[StockBasedataDto] = []
        for company in companies:
            stock_price: StockPrice = db.query(StockPrice).filter(
                StockPrice.ticker == company.ticker).first()
            returned_companies.append(
                StockBasedataDto(ticker=company.ticker, marketCap=company.mktCap, price=stock_price.price))
        return returned_companies

    @staticmethod
    def receive_company_details(company_ticker) -> CompanyProfile:
        company_profile = db.query(CompanyProfile).filter(CompanyProfile.ticker == company_ticker).first()
        if company_profile is None:
            raise NotFoundException("Company not found")
        return company_profile

    @staticmethod
    def receive_companies_select_data() -> list[CompanySelectDataDto]:
        tickers_to_return = []
        company_select_data_list: list = db.query(Company.ticker, Company.name, StockPrice.price).filter(
            Company.ticker == StockPrice.ticker).all()
        for select_data in company_select_data_list:
            tickers_to_return.append(
                CompanySelectDataDto(select_data["name"], select_data["ticker"], select_data["price"]))
        return tickers_to_return