import requests
from sqlalchemy import or_, and_

from publicServer.DTOs.SearchStockDto import SearchStockDto
from publicServer.DTOs.TickerPriceDto import TickerPriceDto
from publicServer.Database.Models.CompanyProfile import CompanyProfile
from publicServer.Database.Models.StockPrice import StockPrice
from publicServer.Database.session import db
from publicServer.config.constants import API_ENDPOINT
from publicServer.config.definitions import KEY_URL
from difflib import SequenceMatcher


def find_most_similar_strings(input_string, string_list):
    ratios = []
    for string in string_list:
        ratio = SequenceMatcher(None, input_string, string).ratio()
        ratios.append((string, ratio))
    sorted_strings = sorted(ratios, key=lambda x: x[1], reverse=True)
    most_similar_strings = [sorted_strings[0][0]]
    for string, ratio in sorted_strings[1:]:
        if ratio == sorted_strings[0][1]:
            if len(most_similar_strings) >= 3:
                break
            most_similar_strings.append(string)
        else:
            break
    return most_similar_strings


class SearchController:
    @staticmethod
    def search_query(query_string) -> list[SearchStockDto]:
        response = requests.get(API_ENDPOINT + "v3/stock-screener?" + query_string + "&" + KEY_URL).json()
        company_profiles = db.query(CompanyProfile.ticker).all()
        companies_to_return = []

        for company1 in company_profiles:
            company1: CompanyProfile
            for company2 in response:
                if company2["symbol"] == company1.ticker:
                    if "marketCap" not in company2:
                        market_cap = "Unknown"
                    else:
                        market_cap = company2["marketCap"]
                    companies_to_return.append(SearchStockDto(len(companies_to_return) + 1, company2["companyName"],
                                                              company2["symbol"], market_cap, company2["beta"],
                                                              company2["price"], company2["sector"]))
                    break
        return companies_to_return

    @staticmethod
    def receive_search_stocks(company) -> list[SearchStockDto]:
        full_company_list = []
        companies = db.query(CompanyProfile.ticker, CompanyProfile.companyName).all()
        for entry in companies:
            full_company_list.append(entry["companyName"])
            full_company_list.append(entry["ticker"])

        similar_strings = find_most_similar_strings(company, full_company_list)
        returned_companies = []
        for string in similar_strings:
            received_company: CompanyProfile = db.query(CompanyProfile.companyName, CompanyProfile.mktCap,
                                                        CompanyProfile.ticker,
                                                        CompanyProfile.sector, CompanyProfile.beta).filter(or_(
                CompanyProfile.ticker == string, CompanyProfile.companyName == string)).first()
            if received_company is None:
                continue

            price = db.query(StockPrice.price).filter(
                StockPrice.ticker == received_company["ticker"]).first()
            returned_companies.append(SearchStockDto(len(returned_companies) + 1, received_company["companyName"],
                                                     received_company["ticker"], received_company["mktCap"],
                                                     received_company["beta"], price["price"],
                                                     received_company["sector"]))
        return returned_companies

    @staticmethod
    def receive_similar_stocks(ticker_list) -> list[TickerPriceDto]:
        similars_to_return = []
        company_list = ticker_list.split(",")
        similar_company_list = []
        companyObject = None
        for company_ticker in company_list:
            companyObject: CompanyProfile = db.query(CompanyProfile).filter(
                CompanyProfile.ticker == company_ticker).first()
            similar_company_list += db.query(CompanyProfile). \
                filter(
                and_(companyObject.sector == CompanyProfile.sector, companyObject.industry == CompanyProfile.industry,
                     CompanyProfile.ticker != companyObject.ticker)).limit(6 - len(similar_company_list)).all()

            if len(similar_company_list) == 6:
                break
        if len(similar_company_list) < 6:
            similar_company_list += db.query(CompanyProfile).filter(and_(CompanyProfile.sector == companyObject.sector,
                                                                         CompanyProfile.ticker != companyObject.ticker)).limit(
                6 - len(similar_company_list)).all()
        similar_stock_price_list: list[StockPrice] = db.query(StockPrice).filter(
            or_(StockPrice.ticker == similar_company_list[0].ticker,
                StockPrice.ticker == similar_company_list[1].ticker,
                StockPrice.ticker == similar_company_list[2].ticker,
                StockPrice.ticker == similar_company_list[3].ticker,
                StockPrice.ticker == similar_company_list[4].ticker,
                StockPrice.ticker == similar_company_list[5].ticker)).all()
        for company in similar_stock_price_list:
            similars_to_return.append(TickerPriceDto(company.ticker, company.change))
        return similars_to_return
